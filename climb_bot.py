# TODO delete own posts if downvoted
# TODO auto-post (instead of being called) route details for a link to mountainproject that someone posted
# TODO email a summary of actions daily
# TODO write a log file instead of only printing to console

import praw
import urllib.parse
from bs4 import BeautifulSoup
import requests
import json
import re
import time
import logging

configpath = 'C:\\projects\\climb_bot\\config.json'  # where to find the config JSON
config = None  # store the JSON loaded from config file


class Route:
    name = ''
    grade = ''
    description = ''
    mpurl = ''

    def __init__(self, name, grade, description, mpurl):
        self.name = name
        self.grade = grade
        self.description = description
        self.mpurl = mpurl

    def __str__(self):
        return ('Route\n\tName: ' + self.name +
                '\n\tGrade: ' + self.grade +
                '\n\tDescription: ' + self.description +
                '\n\tURL: ' + self.mpurl)

    def redditstr(self):
        return ('[' + self.name + ', ' +
                self.grade + ', ' +
                self.description +
                '](' + self.mpurl +
                ') (route on MountainProject.com)')


def findmproute(query):
    '''
    Find the best match for a route on MountainProject.com based on the provided string.
    :param query: String with the query hopefully containing name and location of a route.
    :return: Route object or None if no route was found.
    '''

    searchlink = 'https://www.mountainproject.com/ajax/public/search/results/overview?q=' + urllib.parse.quote(query)
    # "https://www.mountainproject.com/search?q=" + urllib.parse.quote(query)

    name = ''
    grade = ''
    description = ''
    link = None  # initializing the return variable

    r = requests.get(searchlink)
    j = json.loads(r.content.decode('utf-8'))
    if len(j['results']) > 0:
        ajax = j['results']['Routes'][0]
        soup = BeautifulSoup(ajax, 'html.parser')

        name = soup.tr.td.a.string
        grade = soup.find('div', class_='hidden-md-down').strong.string
        description = soup.find('div', class_='hidden-md-down summary').string
        link = 'https://www.mountainproject.com' + soup.tr.td.strong.a['href']

        return Route(name, grade, description, link)

    else:
        return None


def init():
    global config  # JSON loads here

    # configure logging with timestamp and log level
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG, filename='test.log', filemode='a+')
    logging.info('Initializing')

    # TODO error handling for file/config load and authentication
    # print('Loading config: ', configpath)
    logging.info('Loading config: ' + configpath)

    configfile = open(configpath, 'r')
    config = json.load(configfile)
    logging.info('Config loaded')

    # print('Authenticating to Reddit...')
    logging.info('Authenticating to Reddit...')  # TODO don't think it actually auth's yet...
    reddit = praw.Reddit(client_id=config['reddit.client_id'],
                         client_secret=config['reddit.client_secret'],
                         user_agent=config['reddit.user_agent'],
                         username=config['reddit.username'],
                         password=config['reddit.password'])

    # TODO verify auth, write rights - how does PRAW do this, can we force auth now?
    # When offline, PRAW acts like it already auth'd
    if reddit.read_only:
        logging.error('Authentication to Reddit is read-only.')
        raise Exception('Authentication to Reddit is read-only.')
    logging.info('Authentication successful.')  # TODO was it really though?
    logging.info('Initialization complete.')

    return reddit


def main(reddit, subreddit):
    '''
    Execute the logic of the bot. Run after init() is successful.
    :param reddit: PRAW Reddit Object
    :param subreddit: String name of the subreddit to check
    :return: Nothing
    '''
    logging.info('Getting ' + str(config['reddit.commentsPerCheck']) + ' comments from r/' + subreddit)
    for comment in reddit.subreddit(subreddit).comments(limit=config['reddit.commentsPerCheck']):
        match = re.findall('!climb (.*)', comment.body)
        if match:
            logging.info('Found command: ' + match[0] + '    Command in comment: ' + comment.id)
            # TODO record URL to comment. Does PRAW provide?

            file_obj_r = open(config['bot.commentpath'], 'r')

            if comment.id not in file_obj_r.read().splitlines():
                logging.info('Comment ID is unique: ' + comment.id + ' ...retrieving route info and link')
                file_obj_r.close()

                # find the MP route link
                current_route = findmproute(match[0])
                if current_route != None:
                    logging.info('Posting reply to comment: ' + comment.id)
                    comment.reply(current_route.redditstr() + config['bot.footer'])
                    # TODO does PRAW return the comment ID of the reply we just submitted?
                    logging.info('Reply posted to comment: ' + comment.id)
                    logging.info('Opening comment file to record comment: ' + comment.id)
                    file_obj_w = open(config['bot.commentpath'], 'a+')
                    file_obj_w.write(comment.id + '\n')
                    file_obj_w.close()
                    logging.info('Comment file updated with comment: ' + comment.id)
                else:
                    logging.warning('ERROR RETRIEVING LINK AND INFO FROM MP. Comment: ' + comment.id +
                                    '. Body: ' + comment.body)
            else:
                logging.info('Already visited comment: ' + comment.id + ' ...no reply needed.')


if __name__ == '__main__':
    reddit = init()
    count = 0
    while True:
        logging.info('Running bot...')

        for sub in config['bot.subreddits']:
             main(reddit, sub)

        logging.info('Loop count is: ' + str(count))
        print('Count is: ' + str(count))
        count += 1
        logging.info('Sleeping ' + str(config['bot.sleep']) + ' seconds...')
        time.sleep(config['bot.sleep'])

