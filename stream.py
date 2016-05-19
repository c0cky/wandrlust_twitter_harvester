from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    array = []
    with open("keys.txt", "r") as ins:
        for line in ins:
            array.append(line.rstrip('\n'))
    l = StdOutListener()
    auth = OAuthHandler(array[0], array[1])
    auth.set_access_token(array[2], array[3])

    stream = Stream(auth, l)
    stream.filter(track=['business'])