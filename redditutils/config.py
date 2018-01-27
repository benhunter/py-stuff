import json


class Config:
    def __init__(self, json_path=None):
        self.reddit_client_id = ''
        self.reddit_client_secret = ''
        self.reddit_user_agent = ''
        self.reddit_username = ''
        self.reddit_password = ''
        self.reddit_commentsPerCheck = 100
        self.bot_footer = ''
        self.bot_commentpath = ''
        self.bot_logfolder = ''
        self.bot_subreddits = ['test']
        self.bot_sleep = 60
        self.bot_dbname = ''

        if json_path:
            self.load_json(path=json_path)

    def load_json(self, path):
        """
        Load configuration from a JSON file.
        :param path: Path of the JSON file.
        """
        with open(path, 'r') as file:
            config = json.load(file)
        for item in config:
            self.__setattr__(item, config[item])

    def save_json(self, path):
        """
        Save configuration to a JSON file.
        :param path: Path of the JSON file.
        :return:
        """
        with open(path, 'w+') as file:
            json.dump(self.__dict__, file)
