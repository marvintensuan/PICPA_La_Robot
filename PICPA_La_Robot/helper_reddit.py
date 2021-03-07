from praw import Reddit

class RedditInstance():
    '''
    This class will take care of the Reddit instance
    especially with regards to posting.
    '''
    def __init__(self, site_name='', user_agent=''):
        self.site_name = site_name
        self.user_agent = user_agent
        self.Reddit = Reddit(site_name=self.site_name, user_agent=self.user_agent)
        
        self.post_title = ''
        self.post_body = []

    def append_body(self, message, end='\n'):
        if isinstance(message, str):
            self.post_body.append(message + end)
        elif isinstance(message, list):
            self.post_body += message


    def extend_body_last(self, message, end='\n'):
        self.post_body[-1] += message + end

    @property
    def body(self):
        return ''.join(self.post_body)

    def post(self, subreddit):
        self.Reddit.subreddit(subreddit).submit(self.post_title, self.body)

    def comment_on_post(self, comment):
        for post in self.Reddit.redditor(self.site_name).submissions.new(limit=1):
            post.reply(comment)