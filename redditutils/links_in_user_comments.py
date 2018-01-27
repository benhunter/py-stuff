# Print all the links a user has posted in their comments

import logging
import re
import sys

import config
import praw

if sys.platform == 'win32':
    configpath = 'C:/projects/climb_bot/config.json'  # where to find the config JSON
else:
    configpath = './config.json'  # path on linux

config = config.Config(configpath)

logging.info('Authenticating to Reddit...')  # TODO don't think it actually auth's yet...
reddit = praw.Reddit(client_id=config.reddit_client_id,
                     client_secret=config.reddit_client_secret,
                     user_agent=config.reddit_user_agent,
                     username=config.reddit_username,
                     password=config.reddit_password)

# TODO verify auth, write rights - how does PRAW do this, can we force auth now?
# When offline, PRAW acts like it already auth'd
if reddit.read_only:
    logging.error('Authentication to Reddit is read-only.')
    raise Exception('Authentication to Reddit is read-only.')
logging.info('Authentication successful.')  # TODO was it really though?
logging.info('Initialization complete.')

# regex for url: https://regex101.com/r/vT2lF3/1
# simple regex: (?:http(?:s?):\/\/)\S*\.\S*\.\S*
url_regex = re.compile(r'(?:http|https):\/\/((?:[\w-]+)(?:\.[\w-]+)+)(?:[\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?')

name = input("Redditor name: ")

all_the_comments = reddit.redditor(name=name).comments.new(limit=None)
# print(type(all_the_comments))
# print(len(all_the_comments))
comments = []
for c in all_the_comments:
    comments.append(c)
    # print(c)
    match = url_regex.search(c.body)
    if match:
        print(match.group())

print(len(comments), 'comments made')
