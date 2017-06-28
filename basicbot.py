''' Comment reply bot
Author: soujanya_chan
Created: 27 June 2017
Modified: 28 June 2017'''

import praw
USER_AGENT=''
CLIENT_ID=''
CLIENT_SECRET=''
USERNAME=''
PASSWORD=''
SUBREDDIT=''

bot = praw.Reddit(user_agent=USER_AGENT,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        username=USERNAME,
        password=PASSWORD)

subreddit = bot.subreddit(SUBREDDIT)

comments = subreddit.stream.comments()
authors = []

for comment in comments:
    text = comment.body
    author = comment.author
    if 'omg' in text.lower():
        print('found message')
        message = 'OMG, u/{0}, SHOW POWER!!'.format(author)
        comment.reply(message)
    authors.append(comment.author)
