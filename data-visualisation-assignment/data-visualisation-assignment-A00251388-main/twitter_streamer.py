import tweepy
import csv
import twitter_cleanvisua
from twitter_auth_mock import API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
no_of_tweets = 100




def get_tweet_sentiment(tweet):

    analysis = TextBlob(tweet)

    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def get_vader_sentiment(tweet):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(tweet)
    if sentiment_dict['compound'] > 0.05:
        return 'positive'
    elif sentiment_dict['compound'] <= - 0.05:
        return 'negative'
    else:
        return 'neutral'

def get_tweets(query):

    query = query + " -filter:retweets"
    try:
        api.verify_credentials()
        print('Authentication OK')
    except:
        print('Error during Authentication')

    csvFile = open('C:\\Users\\seang\\Desktop\\DataVisualisation\\tweets.csv', 'w')
    csvWriter = csv.writer(csvFile)
    print('Fetching tweets....')
    tweets = api.search(q=query,count = no_of_tweets)
    ##tweets = tweepy.Cursor(api.search, q=query, lang='en').items(no_of_tweets)

    print('Tweets fetching completed')
    print('Writing tweets to file....')
    for t in tweets:
        csvWriter.writerow([t.text.encode('utf-8')])

    print('Writing completed')
    csvFile.close()
    newtweets = []
    for tweet in tweets:
        parsed_tweet = {}
        parsed_tweet['profile_pic'] = tweet.user.profile_image_url
        parsed_tweet['location'] = tweet.user.location
        parsed_tweet['screen_name'] = tweet.user.screen_name
        # saving text of tweet
        parsed_tweet['text'] = tweet.text
        # saving sentiment of tweet
        parsed_tweet['sentimentblob'] = get_tweet_sentiment(tweet.text)
        parsed_tweet['sentimentvader'] = get_vader_sentiment(tweet.text)

        if tweet.retweet_count > 0:
            # if tweet has retweets, ensure that it is appended only once
            if parsed_tweet not in newtweets:
                newtweets.append(parsed_tweet)
        else:
            newtweets.append(parsed_tweet)
    return newtweets