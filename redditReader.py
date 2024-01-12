import praw

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
    
    def isReadOnly(self):
        return self.reddit.read_only
    

