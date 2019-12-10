import tweepy
from tweepy import OAuthHandler
import json


#initializes api
def initialize_tweepy(consumer_key, consumer_secret, access_token, access_secret):
 
    @classmethod
    def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status
     
    # Status() is the data model for a tweet
    tweepy.models.Status.first_parse = tweepy.models.Status.parse
    tweepy.models.Status.parse = parse
    # User() is the data model for a user profil
    tweepy.models.User.first_parse = tweepy.models.User.parse
    tweepy.models.User.parse = parse
    # You need to do it for all the models you need

    try:
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
     
        return tweepy.API(auth)
    except:
        print("Tweepy auth failed")
    

#gets account list from txt file
def get_accounts(filepath):

    name_list = []
    
    with open(filepath) as fp:
        for profile in fp:
            name_list.append(profile)

    print(name_list)

    return name_list


#gets tweet data
def get_tweets(account_name, api):

    tweets = []

    #uses cursor to traverse through all tweets (until it hits the limit)
    for status in tweepy.Cursor(api.user_timeline, screen_name=account_name, tweet_mode="extended").items():
        tweets.append(status)
        print("tweets appended: ", len(tweets))

    return tweets


#get image data from tweet, put it in a set so there are no duplicates
def get_images(tweets):

    image_set = set()
    
    for status in tweets:
        media = status.entities.get('media', [])
        
        if(len(media) > 0):
            image_set.add(media[0]['media_url'])

    return image_set
    

if __name__ == "__main__":
    
    consumer_key = 'LWmcAOW8h8KW7k6bQ5uoDcjQc'
    consumer_secret = '8qkaVo4wGc9H7TYgduCGIO0par6cl7ti7fTvS6pqoGgz47Mj06'
    access_token = '1644845690-M3l9cOmqvVN0e0uNCNZkIHfYEOM76iYQWbimJwT'
    access_secret = 'pNhRXvZ1U2U0WAoQ29i9S5wuhH87jFrNC0BfuDqIPq0QE'

    api = initialize_tweepy(consumer_key, consumer_secret, access_token, access_secret)
    username_list = get_accounts("usernames.txt")
    tweets = []

    for name in username_list:
        tweets += get_tweets(name, api)

    image_set = get_images(tweets)

    for img in image_set:
        print(img)
