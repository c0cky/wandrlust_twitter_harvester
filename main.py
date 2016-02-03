import twitter
import time


array = []

with open("keys.txt", "r") as ins:
    for line in ins:
        array.append(line.rstrip('\n'))
print array
api = twitter.Api(consumer_key=array[0],
                      consumer_secret=array[1],
                      access_token_key=array[2],
                      access_token_secret=array[3])
since_id = 0
wait_time = api.GetAverageSleepTime("/search/tweets")
while (True):
    time.sleep(wait_time)
    results = api.GetSearch(term="travel", since_id=since_id)
    for status in results:
        time.sleep(wait_time)
        print "liking", status
        try:
            api.CreateFavorite(status=status)
        except:
            print "problem liking", status
        since_id = status.id
        with open("statuses.txt", "a") as myfile:
            myfile.write(str(status))
