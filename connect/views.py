import tweepy
from forms import SignInForm, TweetForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from larrypy.settings import CONSUMER_KEY, CONSUMER_SECRET

class SignInView(FormView):
	'''Sign in view for users access'''
	template_name = 'signin.html'
	form_class = SignInForm
	
	def form_valid(self, form):
		auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
		self.success_url = auth.get_authorization_url()
		self.request.session['oauth_request_token_key'] = auth.request_token.key
		self.request.session['oauth_request_token_sec'] = auth.request_token.secret
		return super(FormView, self).form_valid(form)

class RegisterView(View):
	'''Callback view, redirection after Twitter access'''

	def dispatch(self, request, *args, **kwargs):
		req_tok_key = request.session['oauth_request_token_key']
		req_tok_sec = request.session['oauth_request_token_sec']
		ver = request.GET['oauth_verifier']
		tok = request.GET['oauth_token']
		request.session.flush()
		auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
		auth.set_request_token(req_tok_key, req_tok_sec)
		verifiedToken = auth.get_access_token(ver)
		api = tweepy.API(auth)
		User.objects.create_user(myself.screen_name,None,None)
		return redirect