"""Checks Reddit posts for keywords, if found sends a PM.
Author:     doug89
Version:    0.2
Created:    2017-06-24
Modified:   2017-06-24
"""
import praw
import os
import sys

os.chdir(sys.path[0]) # Change the working directory to the script's location.

SUBREDDIT_NAME = 'all'
KEYWORDS = ['dog', 'cat', 'fish', 'bear', 'bird']
RECIPIENT = 'JerzyR'
SUBJECT = 'Keyword Notifier.'
BODY = 'A keyword has been found in a submission.'
GET_LIMIT = None # The number of comments the script will grab for processing.
STREAM_MODE = True # If true the bot will continue indefinitely.

CLIENT_ID = ''
CLIENT_SECRET = ''
USERNAME = ''
PASSWORD = ''
USER_AGENT = 'A script to PM when a keyword is spotted in a post. By /u/doug89'


def main():
    reddit = authenticate()
    start_processing(reddit)


def authenticate():
    """Authenticate into reddit and return a reddit instance."""
    print("Authenticating...")
    reddit = praw.Reddit(user_agent=USER_AGENT,
                         client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                         username=USERNAME, password=PASSWORD)
    print("Authenticaed as {}".format(reddit.user.me()))
    return reddit


def start_processing(reddit):
    """Load a number of submissions, find those with a keyword, and reply."""
    subreddit = reddit.subreddit(SUBREDDIT_NAME)
    processed = read_text_file()
    print('Processing submissions...')
    if STREAM_MODE == True:
        print('Starting stream mode. The bot will work indefinitely as new posts are made.')
        for submission in subreddit.stream.submissions():
            process_submission(submission, reddit, processed)
    else:
        print('Starting batch mode. The bot will work through a batch of posts and stop.')
        for submission in subreddit.new(limit=GET_LIMIT):
            process_submission(submission, reddit, processed)


def process_submission(post, reddit, processed):
    """For each submission, notify or ignore, and add to the processed list."""
    if not post.id in processed:
        all_text = post.title.lower() + '\n\n' + post.selftext.lower()
        has_key = any(k in all_text for k in KEYWORDS)

        if has_key and post.author != reddit.user.me():
            subject = SUBJECT
            body = BODY + '[{}]({})'.format(post.title, post.shortlink)
            try:
                reddit.redditor(RECIPIENT).message(subject, body)
                print('Sent message: {}'.format(post.shortlink))
            except Exception as e:
                print('Error PMing about {}: {}'.format(post.id, e))

        processed.append(post.id)
        append_text_file(post.id)


def read_text_file():
    """Open a text file and assign its contents to a list."""
    try:
        with open("id_list.txt", "r") as file:
            processed = file.read().split('\n')
        # Remove old and now irrelevant IDs. Keeps the text file tidy.
        if len(processed) > 20000:
            processed = processed[-10000:]
            with open("id_list.txt", "w") as file:
                file.write('\n'.join(processed))

    except (OSError, IOError):
        processed = []
    return processed


def append_text_file(post_id):
    """Take a string and append it to a text file."""
    with open('id_list.txt', 'a') as file:
        file.write(post_id + '\n')


if __name__ == '__main__':
    main()
