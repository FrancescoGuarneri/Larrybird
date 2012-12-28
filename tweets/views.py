import tweepy
from models import Tweep
from sec import CONSUMER_KEY, CONSUMER_SECRET, USER_PASSWORD
from forms import SignInForm, TweetForm
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.generic.edit import FormView


class SignInView(FormView):
	'''Sign in view for users access'''
	template_name = 'home.html'
	form_class = SignInForm
	
	def form_valid(self, form):
		logout(self.request)
		if not self.request.user.is_authenticated():
			#If the user is not already logged in
			auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)			
			self.success_url = auth.get_authorization_url()
			self.request.session['oauth_request_token_key'] = auth.request_token.key
			self.request.session['oauth_request_token_sec'] = auth.request_token.secret
			return super(FormView, self).form_valid(form)
		else:
			return redirect('/tweet/')
		
class RegisterView(View):
	'''Callback view, redirection after Twitter access'''

	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated():
			#Get request tokens from the current session
			req_tok_key = request.session['oauth_request_token_key']
			req_tok_sec = request.session['oauth_request_token_sec']
			#Retrieve the new token and the verifier from twitter
			ver = request.GET['oauth_verifier']
			#Clean the current session
			request.session.flush()
			#Start a new authentication object and set its request tokens
			auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
			auth.set_request_token(req_tok_key, req_tok_sec)
			#Pass the verifier to the auth instance and create a new api
			verifiedToken = auth.get_access_token(ver)
			api = tweepy.API(auth)
			user_name = api.me().screen_name 
			#Look in the database for an existing user with user_name
			tweep_match = Tweep.objects.filter(username = user_name)
			if tweep_match.count() == 0:
				#Register a new user on Larrypy with twitter Username and save its tokens
				tweep = Tweep.objects.create_user(user_name, None, USER_PASSWORD)
				tweep.access_token = auth.access_token.key
				tweep.access_secret = auth.access_token.secret
				tweep.save()
				#tweep.change_tokens(auth.access_token.key,auth.access_token.secret)
				#Finally login the user and redirect him to the main site area
				user = authenticate(username = user_name, password = USER_PASSWORD)
				login(request, user)
				return redirect('/tweet/')
			elif tweep_match.count() == 1:
				#If there is almost an user already registerd, just change his tokens again and login
				for tweep in tweep_match:
					tweep.access_token = auth.access_token.key
					tweep.access_secret = auth.access_token.secret
					tweep.save()
					user = authenticate(username = user_name, password = USER_PASSWORD)
					login(request, user)
				return redirect('/tweet/')
		else:
			#If the user is already authenticated, redirect him to the main site area
			return redirect('/tweet/')


class SendTweets(FormView):
	'''Send tweets from a simple form'''
	template_name = 'tweet.html'
	form_class = TweetForm
	success_url = '/tweet/'
	api = None

	def dispatch(self, request, *args, **kwargs):
		#Find the user object in the database
		if not request.user.is_authenticated():
			return redirect('/signin/')
		else:
			tweep = Tweep.objects.filter(username=request.user.username)
			auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
			auth.set_access_token(tweep[0].access_token,tweep[0].access_secret)
			self.api = tweepy.API(auth)
			return super(FormView, self).dispatch(request)

	def form_valid(self, form): 
		if len(form['tweet']) < 141:
			self.api.update_status(form.cleaned_data['tweet'])
			return super(FormView, self).form_valid(form)
		else:
			return redirect('/tweet/')