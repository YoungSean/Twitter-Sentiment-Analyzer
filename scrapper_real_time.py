import tweepy
import pandas as pd

api_key = "DYOuY4pgi4uBBQW2vVZwG0hfU"
api_secret = "xfce6lOPz1TbWO8gINgS4cUVgCQ0HEmSyDwsFKje5jTJD4nY7D"
access_key = "931114843532279809-ZrSYSt0zE1H1nZE5eR25PgCuhxIXRO2"
access_secret = "NUofJHTz7RLjkj7MwMkwvTxIVe1hhpSPIPtLLnci9vDeP"

auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#
# # get the home timeline tweets
# timelines = api.home_timeline()
# #print(timelines[0]._json["text"])
#
# for i in range(5):
#     print(timelines[i]._json["text"])

### Use hashtag to search tweets
#
# tw_keyword = "#DemonSlayer"
# num_tweets = 10
#
# tweets = tweepy.Cursor(api.search_tweets, q=tw_keyword, tweet_mode="extended").items(num_tweets)
# print(tweets)
#
#
# ## make a data frame
# columns = ['User', 'Tweet Text', 'hashtags']
# data = []
# for t in tweets:
#     uname = t.user.screen_name
#     content = t.full_text
#     hashtags = t.entities['hashtags']
#     data.append([uname, content, hashtags])
#
# df = pd.DataFrame(data, columns=columns)
# df.to_csv(tw_keyword[1:]+"_tweet.csv")
# print(df)

### Get real time tweets
# reference:
# stream: https://docs.tweepy.org/en/stable/stream.html
class Tweet_Listener(tweepy.Stream):

    tweets = []
    num_limit = 3


    def on_status(self, status):
        # treat status as a tweet object
        # tweet object: https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet

        self.tweets.append(status)
        #print(str(status.created_at) +"\tuser: "+status.user.screen_name + "\t:"+status.text)
        print("got one tweet")

        # once the number of tweets collected is equal to num_limit,
        # we stop the streaming
        if len(self.tweets) == self.num_limit:
            self.disconnect()


stream_tweets = Tweet_Listener(api_key, api_secret, access_key, access_secret)

tw_keyword = ["#blacklivesmatter"]
languages = ["en"]

stream_tweets.filter(track=tw_keyword, languages=languages)

result = []

for tweet in stream_tweets.tweets:
    if tweet.truncated:
        content = tweet.extended_tweet["full_text"]
    else:
        content = tweet.text

    result.append([tweet.user.screen_name, content])

print(result)

