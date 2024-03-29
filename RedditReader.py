import praw

# Helper class to utilize python reddit wrapper more conveniently
class redditReader:

    def __init__(self, client_id, client_secret, user_agent):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent

        self.reddit = praw.Reddit(
            client_id= self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )
    
    def __init__(self):
        self.reddit = praw.Reddit("user")
    
    def isReadOnly(self):
        return self.reddit.read_only
    
    def getNewPost(self, subreddit, mode, time, num_posts):
        if mode == "top":
            return self.reddit.subreddit(subreddit).top(time_filter=time,limit=num_posts)

