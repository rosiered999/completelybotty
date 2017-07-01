''' Bans users permanently if a mod comments on a comment '+ban' also removes the '+ban' and the offending comment
Author: soujanya_chan
Created: 28 June 2017
Modified: 1 July 2017'''

import praw
import os
from time import gmtime, strftime

USER_AGENT=''
CLIENT_ID=''
CLIENT_SECRET=''
USERNAME=''
PASSWORD=''
SUBREDDIT='morbidreality'
LIMIT=100
LEVEL = 0

def authenticate():
    bot = praw.Reddit(user_agent=USER_AGENT,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=USERNAME,
            password=PASSWORD)
    print('Authenticated as /u/{0}'.format(bot.user.me()))
    return bot

def ban(user,mod_that_banned,SUBREDDIT,bot,ban_msg,top_level_comment,parent):
    ban_list = bot.subreddit(SUBREDDIT).banned()
    if mod_that_banned in bot.subreddit(SUBREDDIT).moderator() and user not in ban_list:
        print('banned /u/{0}'.format(user.name))
        print('banned by /u/{0}'.format(mod_that_banned))
        if ban_msg=='':
            bot.subreddit(SUBREDDIT).banned.add(user.name)
            print('no ban msg')
        else:
            bot.subreddit(SUBREDDIT).banned.add(user.name, ban_reason=ban_msg)
            print('Banned for:')
            print(ban_msg)
        bot.comment(top_level_comment.id).mod.remove(spam=False)
        bot.comment(parent).mod.remove(spam=False)
    print('\n\n\n')

def list_ban(bot):
    for ban in bot.subreddit(SUBREDDIT).banned():
        print('{}: {}'.format(ban, ban.note))

def dfs(submission, forest_comments,LEVEL,SUBREDDIT,bot,PARENTS,ban_msg):
    if not os.path.isfile("done_bans_coms.txt"):
        done_bans_coms = []
    else:
        with open("done_bans_coms.txt", "r") as f:
            done_bans_coms = f.read()
            done_bans_coms = done_bans_coms.split('\n')
            done_bans_coms = list(filter(None,done_bans_coms))

    LEVEL = LEVEL+1
    ban_list = bot.subreddit(SUBREDDIT).banned()
    visited = []
    for top_level_comment in forest_comments:
        if top_level_comment not in visited:
            visited.append(top_level_comment)
            next_level = top_level_comment
            if type(top_level_comment).__name__ == "MoreComments":
                next_level = next_level.comments()
            elif type(top_level_comment).__name__=="Comment":
                parent = top_level_comment.parent().fullname.split('_')[1]
                next_level = top_level_comment.replies
                text = top_level_comment.body.split(' ')
               # print(text)

                if '+ban' in text and parent!=submission.id and top_level_comment.id not in done_bans_coms:
                    if len(text)>1:
                        for i in range(1,len(text)-1):
                            ban_msg += text[i] + ' '
                        ban_msg += text[i+1]
                    else:
                        ban_msg = ''
                    mod_that_banned = top_level_comment.author
                    user = bot.comment(parent).author
                    ban(user,mod_that_banned,SUBREDDIT,bot,ban_msg,top_level_comment,parent)
                dfs(submission, next_level,LEVEL,SUBREDDIT,bot,PARENTS,ban_msg)


def parse(reddit):
    ban_msg =''
    current =''
    PARENTS= []
    if not os.path.isfile("done_banning.txt"):
        done_banning = []
    else:
        with open("done_banning.txt", "r") as f:
            done_banning = f.read()
            done_banning = done_banning.split('\n')
            done_banning = list(filter(None,done_banning))
    subreddit = reddit.subreddit(SUBREDDIT)
    #print(subreddit.display_name)

    for submission in subreddit.new(limit=None):#stream.submissions():
        forest_comments = submission.comments
        dfs(submission,forest_comments,LEVEL,SUBREDDIT,reddit,PARENTS,ban_msg)


def main():
    reddit = authenticate()
    parse(reddit)

if __name__ =='__main__':
    main()
