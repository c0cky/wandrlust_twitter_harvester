import twitter
import time
import getopt
import sys
import tweepy
import csv


def harvest(query, out_file):
    array = []
    with open("keys.txt", "r") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))
    print array
    api = twitter.Api(consumer_key=array[0],
                      consumer_secret=array[1],
                      access_token_key=array[2],
                      access_token_secret=array[3],
                      sleep_on_rate_limit=True)
    like = twitter.Api(consumer_key=array[0],
                      consumer_secret=array[1],
                      access_token_key=array[2],
                      access_token_secret=array[3])
    since_id = 0
    while (True):
        results = api.GetSearch(term=query, since_id=since_id, count=100, result_type="recent")
        for status in results:
            like.CreateFavorite(id=status.id)
            since_id = status.id
            with open(out_file, "a") as myfile:
                myfile.write(str(status) + '\n')

def create_friends(query):
    array = []
    with open("keys.txt", "r") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))
    print array
    api = twitter.Api(consumer_key=array[0],
                      consumer_secret=array[1],
                      access_token_key=array[2],
                      access_token_secret=array[3])
    if query == "":
        query = "early adopter"
    people = []
    for i in range(2, 5):
        people += api.GetUsersSearch(term=query, count=20, page=i)
    print len(people)
    for p in people:
        print p.GetScreenName()
        api.CreateFriendship(user_id=p.GetId())


def get_user_tweets(screen_name):
    array = []
    with open("keys.txt", "r") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))
    print array
    auth = tweepy.OAuthHandler(array[0], array[1])
    auth.set_access_token(array[2], array[3])
    api = tweepy.API(auth)
    alltweets = []
	#make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)

	#save most recent tweets
    alltweets.extend(new_tweets)

	#save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

	#keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print "getting tweets before %s" % (oldest)

		#all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
        alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

	#write the csv
    with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets)

    pass

def followers_list():
    array = []
    with open("keys.txt", "r") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))
    print array
    api = twitter.Api(consumer_key=array[0],
                      consumer_secret=array[1],
                      access_token_key=array[2],
                      access_token_secret=array[3])
    followers = api.GetFollowerIDs()
    friends = api.GetFriendIDs()
    un_friend_list = list(set(friends) - set(followers))
    print len(followers)
    print len(friends)
    for x in un_friend_list:
        print x
        api.DestroyFriendship(user_id=x)
    print "unfollowed : " ,len(un_friend_list)

def followup(file):
    array = []
    with open("keys.txt", "r") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))
    print array
    api = twitter.Api(consumer_key=array[0],
                      consumer_secret=array[1],
                      access_token_key=array[2],
                      access_token_secret=array[3])
    followers = api.GetFollowerIDs()
    import json
    tweets = []
    with open(file) as data_file:
        for line in data_file:
            data = json.loads(line)
            tweets.append(data)
    followup = []
    for t in tweets:
        if t["user"]["id"] in followers:
            x = api.GetUser(user_id=t["user"]["id"])
            followup.append(x.screen_name)
    followup = sorted(set(followup))
    for f in followup:
        print f

def main(argv):
    command = ""
    query = ""
    file = ""
    try:
        opts, args = getopt.getopt(argv, "helps:w:i:", ["command=", "query=", "file="])
    except getopt.GetoptError:
        print "main.py --command <command> --query <query> --file <file_file>"
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print "main.py --command <command> --query <query> --file <file>"
            sys.exit()
        elif opt in ("-c", "--command"):
            command = arg
        elif opt in ("-q", "--query"):
            query = arg
        elif opt in ("-o", "--file"):
            file = arg

    if not file:
        file = "statuses.json"
    print command
    if command == "harvest":
        print "harvest"
        harvest(query, file)
    elif command == "followup":
        followup(file)
    elif command == "followers":
        followers_list()
    elif command == "create":
        create_friends(query)
    elif command == "user":
        get_user_tweets(query)
    elif command == "":
        print "main.py --command <command> --query <query> --file <file>"
        sys.exit()

    print "FINISHED!"

main(sys.argv[1:])