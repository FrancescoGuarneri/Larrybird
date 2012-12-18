#!/usr/bin/env python

import tweepy

def get_hundred_tweets(user_api,user_id):
	'''Get a Tweet list of the last 1000 tweets of an user given his id'''
	tweets = []
	for result in tweepy.cursor.Cursor(user_api.user_timeline, include_rts=True, id=user_id).items():
		tweets += [result]
	return tweets


def get_following(user_api, user_id):
	'''Get an User list of the tweeps an user follows given his id'''
	following = []
	for result in tweepy.cursor.Cursor(user_api.friends,id=user_id).items():
		following += [result]	
	return following


def get_followers(user_api, user_id):
	'''Get an User list of the people who follows an user given his id'''
	following = []
	for result in tweepy.cursor.Cursor(api.followers,id=user_id).items():
		following += [result]
	return following


def match_followers(user_api, user, other_user):
	'''Check differences between followings and followers'''
	follo1 = getFollowing(user_api, user.id)
	follo2 = getFollowers(user_api, other_user.id)
	common = []
	unCommon = []
	for f1 in follo1:
		ID1 = f1.id
		for f2 in follo2:
			ID2 = f2.id
			if ID1==ID2:
				common += [f1]
				#Only one follower can match
				break 
	for f in follo1:
		if f not in common:
			unCommon += [f]
	return [common,unCommon]


def unfollow(user_api, user_id):
	'''Unfollow an user given his id'''
	user_api.destroy_friendship(user_id)
	

def mass_direct_message(user_api, dm_text, follwers_list):
	'''Send a DM to all your followers'''
	for follower in followers_list:
		try:
			receiver_id = follower.id
			user_api.send_direct_message(user_id=receiver_id,text=dm_text)
		except:
			pass
	

def save_tweets_in_file(tweets_list,path):
	'''Saves a tweets list on a text file'''
	lenght = len(tweets_list)
	name = user.screen_name
	tweets_file = open(path + 'tweets.txt','w')
	tweets = []
	for tweet in tweets_list:
		try:
			tweets += [str(tweet.text)+'\n\n']
		except:
			pass
	tweets_file.write('THESE ARE THE LAST ' + str(lenght) +' TWEETS\n')
	tweets_file.write('===============================\n')
	tweets_file.writelines(tweets)
	tweets_file.close()