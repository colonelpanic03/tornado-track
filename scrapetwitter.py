import tweepy # tweepy module to interact with Twitter
import pandas as pd # Pandas library to create dataframes
from tweepy import OAuthHandler # Used for authentication
from tweepy import Cursor # Used to perform pagination
import sys

cons_key = "HIDDEN"
cons_secret = "HIDDEN"
acc_token = "HIDDEN"
acc_secret = "HIDDEN"

# (1). Athentication Function
def get_twitter_auth():
    """
    @return:
        - the authentification to Twitter
    """
    try:
        consumer_key = cons_key
        consumer_secret = cons_secret
        access_token = acc_token
        access_secret = acc_secret
        
    except KeyError:
        sys.stderr.write("Twitter Environment Variable not Set\n")
        sys.exit(1)
        
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    
    return auth

# (2). Client function to access the authentication API
def get_twitter_client():

    auth = get_twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client
    
# (3). Function creating final dataframe
def get_tweets_from_user(words, page_limit=16, count_tweet=200):

    client = get_twitter_client()

    all_tweets = [] 
    
    for page in Cursor(client.search_tweets, 
                        words, lang="en", 
                        count=count_tweet).pages(page_limit):
        for tweet in page:
            parsed_tweet = {}
            parsed_tweet['Date & Time'] = tweet.created_at
            parsed_tweet['Username'] = tweet.user.screen_name
            parsed_tweet['Tweet Text and Link'] = tweet.text
            parsed_tweet['Likes'] = tweet.favorite_count
            parsed_tweet['Retweets'] = tweet.retweet_count
                
            all_tweets.append(parsed_tweet)
    
    # Create dataframe 
    df = pd.DataFrame(all_tweets)
    
    # Revome duplicates if there are any
    df = df.drop_duplicates( "Tweet Text and Link" , keep='first')


    df.to_html('templates/TornadoResults.html')

    return df

# keywords = get_tweets_from_user("tornado")

# print("Data Shape: {}".format(keywords.shape))
