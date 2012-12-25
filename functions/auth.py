#!/usr/bin/env python

import tweepy



def user_access(auth, ACCESS_KEY, ACCESS_SECRET):
    '''Prepare an API object for the user'''
    auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)
    api = tweepy.API(auth)
    return api