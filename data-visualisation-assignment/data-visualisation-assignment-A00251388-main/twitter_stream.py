import os
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import twitter_auth_mock
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
class TwitterClient(object):

    def __init__(self, query):

        try:
            self.auth = OAuthHandler(twitter_auth_mock.API_KEY, twitter_auth_mock.API_SECRET)
            self.auth.set_access_token(twitter_auth_mock.ACCESS_TOKEN, twitter_auth_mock.ACCESS_TOKEN_SECRET)
            self.query = query
            self.api = tweepy.API(self.auth)
            self.tweet_count_max = 100
        except:
            print("Authentication Failed")

    def set_query(self, query=''):
        self.query = query

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_vader_sentiment(self,tweet):
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(self.clean_tweet(tweet))
        if sentiment_dict['compound'] >= 0.05:
            return 'positive'
        elif sentiment_dict['compound'] <= - 0.05:
            return 'negative'
        else:
            return 'neutral'


    def get_tweets(self):
        tweets = []

        try:
            recd_tweets = self.api.search(q=self.query,count=self.tweet_count_max) #, lang=['en'])
            if not recd_tweets:
                pass
            for tweet in recd_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['user'] = tweet.user.screen_name
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                parsed_tweet['sentimentvader'] = self.get_vader_sentiment(tweet.text)

                if "Android" in tweet.source:
                    parsed_tweet['phone'] = 'Android'
                elif "iPhone" in tweet.source:
                    parsed_tweet['phone'] = 'iPhone'
                else:
                    parsed_tweet['phone'] = 'Other'

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
