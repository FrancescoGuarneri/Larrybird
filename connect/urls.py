from django.conf.urls import patterns, url
from views import SignInView, RegisterView

urlpatterns = patterns('',
    url(r'^signin/', SignInView.as_view()),
    url(r'^register/', RegisterView.as_view()),
)