import time
import tweepy
from setup.settings import TwitterSettings
from models.tweet import TweetModel


class FStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.start_time = time.time()
        self.limit = TwitterSettings.get_instance().stream_time

        super(FStreamListener, self).__init__()

    def on_status(self, status):
        if (time.time() - self.start_time) < self.limit:

            # Create tweet object
            forttweet = TweetModel(
                status.source,
                status.user.name,
                status.user.profile_background_image_url_https,
                status.text,
                status.created_at,
                status.user.location,
            )

            forttweet.insert()

            return True
        else:
            # TODO Use Logger instead
            print("Live capture has stopped")

            # Stop the loop of streaming
            return False

    def on_error(self, status):
        raise Exception(f"An error occurred while fetching tweets: {status}")
