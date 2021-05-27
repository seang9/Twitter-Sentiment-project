from flask import Flask, render_template, request,jsonify
import twitter_stream
import twitter_cleanvisua

app = Flask(__name__)
nam = twitter_stream.TwitterClient('')
new = twitter_stream.TwitterClient('')

@app.route('/')
def index():
    return render_template('results.html')

@app.route('/tweets')
def tweets():
    query = request.args.get('query')
    Secondqury = request.args.get('2query')
    nam.set_query(query)
    new.set_query(Secondqury)
    tweets = nam.get_tweets()
    sdata = new.get_tweets()
    return jsonify({'data': tweets, 'sdata': sdata,'query':query,'Secondqury':Secondqury, 'count': len(tweets),'secondcount': len(sdata)})

@app.route('/api')
def hello_world():
    tweetlist =twitter_cleanvisua.main()
    ##twitter_cleanvisua.graph(tweetlist)
    ##twitter_cleanvisua.graph2(tweetlist)
    ##textblob = "static/TextBlob.png"
    ##vader = "static/Vader.png"
    print(tweetlist)
    return render_template('index.html', tweetlist=tweetlist)



if __name__ == '__main__':
    app.run()