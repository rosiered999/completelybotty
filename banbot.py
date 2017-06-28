import praw
import os
from time import gmtime, strftime

USER_AGENT=''
CLIENT_ID=''
CLIENT_SECRET=''
USERNAME=''
PASSWORD=''
SUBREDDIT=''
LIMIT=10


def authenticate():
    bot = praw.Reddit(user_agent=USER_AGENT,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            username=USERNAME,
            password=PASSWORD)
    print('Authenticated as /u/{0}'.format(bot.user.me()))
    return bot

def ban(user,mod_that_banned,SUBREDDIT,bot,ban_msg):
    ban_list = bot.subreddit(SUBREDDIT).banned()
    for subreddit in bot.user.moderator_subreddits():
        if subreddit.display_name == SUBREDDIT and user not in ban_list:
            print('banned /u/{0}'.format(user.name))
            print('banned by /u/{0}'.format(mod_that_banned))
            if ban_msg=='':
                bot.subreddit(SUBREDDIT).banned.add(user.name)
                print('no ban msg')
            else:
                bot.subreddit(SUBREDDIT).banned.add(user.name, ban_reason=ban_msg)
                print('Banned for:')
                print(ban_msg)
    print('\n\n\n\n\n\n\n')

def list_ban(bot):
    for ban in bot.subreddit(SUBREDDIT).banned():
        print('{}: {}'.format(ban, ban.note))

def parse(reddit):
    ban_msg =''
    if not os.path.isfile("done_banning.txt"):
        done_banning = []
    else:
        with open("done_banning.txt", "r") as f:
            done_banning = f.read()
            done_banning = done_banning.split('\n')
            done_banning = list(filter(None,done_banning))
    subreddit = reddit.subreddit(SUBREDDIT)
    #print(subreddit.display_name)

    for submission in subreddit.new(limit=LIMIT):#stream.submissions():
        if submission.id not in done_banning:
            #print(submission.title)
            #print(submission.id)
            redditor = submission.author
            #print(redditor.name)
            all_comments = submission.comments.list()
            #print(all_comments)
            for comment in all_comments:
                text = comment.body
                if '+ban' in comment.body:
                    text = comment.body.split(' ')
                    if len(text)>1:
                        #print(text[1])
                        for i in range(1,len(text)-1):
                            ban_msg += text[i]+' '
                        ban_msg += text[i+1]
                    else:
                        ban_msg = ''
                    mod_that_banned = comment.author
                    ban(redditor,mod_that_banned,SUBREDDIT,reddit,ban_msg)
                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    with open("done_banning.txt", "w") as f:
                        f.write(submission.id+' '+ban_msg+' '+time+'\n')
                    list_ban(reddit)


def main():
    reddit = authenticate()
    parse(reddit)

if __name__ =='__main__':
    main()
