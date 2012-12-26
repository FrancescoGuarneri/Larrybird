from django import forms

class SignInForm(forms.Form):
	pass

class TweetForm(forms.Form):
	tweet = forms.CharField(140)

