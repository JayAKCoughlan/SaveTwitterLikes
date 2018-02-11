def finishIt(saved_list):
    print("Closing Program")
    f = open("save.txt", "w+")
    for id in saved_list:
        f.write(id)
    f.close()
    quit()

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import *
#import the wget library to download the images
import wget
#import the system library
import sys
#import os library
import os

#print(len(sys.argv))

#first we open the file we want to save our "last grabbed tweets", we're just saving the last three tweet id's, this way if one is deleted, 
#we don't download a bunch of tweet pics we already have
save_limit = 3
if(len(sys.argv) > 1):
    if(sys.argv[1].isdigit()):
        save_limit = int(sys.argv[1])
        print("setting save limit is " + sys.argv[1])
    

#This is for if we want to ignore the saved tweets
ignore_save = False
if(len(sys.argv) > 2):
    if(sys.argv[2].lower() == 'false'):
        ignore_save = False
        print("setting ignore save to false")
    elif (sys.argv[2].lower() == 'true'):
        ignore_save = True
        print("setting ignore save to true")

#This is for the number of tweets we want to pull
tweet_pull = 5
if(len(sys.argv) > 3):
    if(sys.argv[3].isdigit()):
        tweet_pull = int(sys.argv[3])
        print("setting tweets to pull " + sys.argv[3])

#this is for the folder we want to put the images in
image_dest = 'D:\\~User\\Projects\\savetwitterimage\\images\\'
#D:\\~User\\Projects\\savetwitterimage\\images\\ PC
#C:\\Users\\Jay\\Documents\\Projects\\savetwitterimage\\images\\ laptop
if(len(sys.argv) > 4):
    image_dest = sys.argv[4]

#This is for the tweet we want to search from. We require a Tweet_ID
pull_from = "NON"
if(len(sys.argv) > 5):
    pull_from = sys.argv[5]


f = open("save.txt", "r") #we're opening with write mode so that when we save our new tweets, we can save them direct to the file
#now we're going to apply what we read in to this list
saved = f.readlines()
f.close()
#f = open("save.txt", "w+")
# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = 'YOUR TOKEN HERE'
ACCESS_SECRET = 'YOUR TOKEN HERE'
CONSUMER_KEY = 'YOUR TOKEN HERE'
CONSUMER_SECRET = 'YOUR TOKEN HERE'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter Streaming API
twitter_stream = Twitter(auth=oauth)

# Get a sample of the public data following through Twitter
if(pull_from != "NON"):
    try:
        iterator = twitter_stream.favorites.list(screen_name="JayAKCoughlan", count=tweet_pull, max_id=pull_from)
    except:
        print ("Twitter ID " + pull_from + " does not appear to exist or is unreadable")
        raise
elif (ignore_save == False and len(saved) >= 1):
    iterator = twitter_stream.favorites.list(screen_name="JayAKCoughlan", count=tweet_pull, since_id=saved[0])
else:
    iterator = twitter_stream.favorites.list(screen_name="JayAKCoughlan", count=tweet_pull)

# Print each tweet in the stream to the screen 
# Here we set it to stop after getting 1000 tweets. 
# You don't have to set it to stop, but can continue running 
# the Twitter API to collect data for days or even longer. 
tweet_count = tweet_pull
counter = 0
for tweet in iterator:
    #print(json.dumps(tweet))
    if(len(saved) > 0 and ignore_save == False):
        #print("\ngreater than none")
        for tweet_id in saved:
            #tweet_id.strip('\n')
            #print(tweet_id[:-1])
            #print(tweet['id_str'])
            if(tweet_id[:-1] == tweet['id_str']):
                print("\nFound a match. Exiting...")
                finishIt(saved)
    
    #now since we didn't break, we save the first three to the saved file
    if(counter < save_limit):
        id_str = tweet['id_str'] + '\n'
        #this causes recently seen tweets to be checked against later saved tweets. 
        #It should not be an issue since you shouldn't see the same tweet twice in a run
        saved = [id_str] + saved

    # Twitter Python Tool wraps the data returned by Twitter 
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    if( 'extended_entities' in tweet):
        media = tweet['extended_entities'].get('media', []) #extended_entities actually has ALL the media links. Entities only has the first
        
    elif( 'entities' in tweet):
        media = tweet['entities'].get('media', [])
    
    #go through all the media on the tweet and download it
    for iii in range(0,  len(media)):

        #download the image immediately
        wget.download(media[iii]['media_url'], out=image_dest)

        #split the path so we get just the name
        media_name = media[iii]['media_url'].split('/')
        #create the original file name plus path
        original_name = image_dest + media_name[-1]
        split_name = media_name[-1].split('.')
        new_name = image_dest + tweet['user'].get('screen_name') + "_" + media_name[-1]

        #if we find the file already exists, we'd rather save a duplicate
        duplicate = 1
        while(os.path.isfile(new_name)):
            new_name = image_dest + tweet['user'].get('screen_name') + "_" + split_name[0] + "(" + str(duplicate) + ")." + split_name[1]
            duplicate += 1

        os.rename(original_name, new_name)
        #print(media_name[-1])


    # The command below will do pretty printing for JSON data, try it out
    #print json.dumps(tweet, indent=4)
    counter += 1
    if tweet_pull <= counter:
        print("\nReached end of tweet list. Exiting...")
        #f.close()
        finishIt(saved[:save_limit])
        #break
print("Reached end of Iterator")
finishIt(saved[:save_limit])