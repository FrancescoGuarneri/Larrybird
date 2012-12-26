from django.conf.urls import patterns, url
from views import SignInView, RegisterView, SendTweets

urlpatterns = patterns('',
    url(r'^signin/', SignInView.as_view()),
    url(r'^register/', RegisterView.as_view()),
    url(r'^tweet/', SendTweets.as_view()),
)