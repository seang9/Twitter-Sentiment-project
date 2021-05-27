
from textblob import TextBlob
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import twitter_streamer

searchTerm = "pfizer"
noOfSearches = 100

def percentage(part, whole):
    return 100 * part / whole

def blob_sentiment_scores(tweets):
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    counter = 0
    for tweet in tweets:
        analysis = TextBlob(tweet['text'])
        polarity += analysis.sentiment.polarity
        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
        elif (analysis.sentiment.polarity > 0.00):
            positive += 1
        counter +=1

    positive = percentage(positive, counter)
    negative = percentage(negative, counter)
    neutral = percentage(neutral, counter)
    positive = format(round(positive), '2f')
    negative = format(round(negative), '2f')
    neutral = format(round(neutral), '2f')
    print(counter)
    return positive, negative, neutral

def vader_sentiment_scores(tweets):

    positives = 0
    negatives = 0
    neutrals = 0
    counter = 0
    sid_obj = SentimentIntensityAnalyzer()
    for tweet in tweets:
        print(tweet['text'])
        sentiment_dict = sid_obj.polarity_scores(tweet['text'])
        if sentiment_dict['compound'] >= 0.05:
            positives += 1
        elif sentiment_dict['compound'] <= - 0.05:
            negatives += 1
        else:
            neutrals += 1
        counter += 1

    positives = percentage(positives, counter)
    negatives = percentage(negatives, counter)
    neutrals = percentage(neutrals, counter)
    positives = format(round(positives), '2f')
    negatives = format(round(negatives), '2f')
    neutrals = format(round(neutrals), '2f')
    return positives, negatives, neutrals

def graph(tweets):
    positive, negative, neutral =blob_sentiment_scores(tweets)
    labels = ['Positive [' + str(positive) + '%]', 'Negative [' + str(negative) + '%]',
              'Neutrals [' + str(neutral) + '%]']
    size = [positive, negative, neutral]
    colors = ['yellowgreen', 'gold', 'red']
    patches, text = plt.pie(size, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("TextBlob Reaction: " +"People Reaction to "+ searchTerm + " Tweets")
    plt.axis('equal')
    plt.tight_layout()

    plt.savefig('./static/TextBlob.png')
    plt.show()


def graph2(tweets):
    positives, negatives, neutrals = vader_sentiment_scores(tweets)
    labels = ['Positive [' + str(positives) + '%]', 'Negative [' + str(negatives) + '%]',
              'Neutrals [' + str(neutrals) + '%]']
    size = [positives, negatives, neutrals]
    colors = ['yellowgreen', 'gold', 'red']
    patches, text = plt.pie(size, colors=colors, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.title("Vader Reaction: " +"People Reaction to "+ searchTerm + " Tweets")
    plt.axis('equal')
    plt.tight_layout()

    plt.savefig('./static/Vader.png')
    plt.show()


def main():
    tweets = twitter_streamer.get_tweets(searchTerm)
    ##graph(tweets)
    ##graph2(tweets)
    return tweets

if __name__ == '__main__':
    main()