#!/usr/bin/python
import twitter
import time
import getopt
import sys

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
    since_id = 0
    while (True):
        results = api.GetSearch(term=query, since_id=since_id, count=100, result_type="recent")
        for status in results:
            try:
                api.CreateFavorite(id=status.id)
            except:
                print "problem liking", status.id
            since_id = status.id
            with open(out_file, "a") as myfile:
                myfile.write(str(status) + '\n')

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
    elif command == "":
        print "main.py --command <command> --query <query> --file <file>"
        sys.exit()
    
    print "FINISHED!"

main(sys.argv[1:])