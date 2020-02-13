import time
import config
import telebot
import praw

try:

    bot = telebot.TeleBot(config.tg_token)

    reddit = praw.Reddit(client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent=config.user_agent)

    already_posted_list = []
    gonna_post_list = []
    incoming_list = []

    while (true):
        gonna_post_list.clear()
        incoming_list = reddit.subreddit('memes').hot(limit=10)
        print("Incoming list: ")
        print(incoming_list)
        for new in reddit.subreddit('memes').hot(limit=10):
            flag = 0
            for old in already_posted_list:
                if old.name == new.name:
                    flag = 1
                    print("OLD POST! " + old.name)
            if flag == 0:
                gonna_post_list.append(new)

        for fresh_image in gonna_post_list:
            bot.send_photo(config.tg_channelID, fresh_image.url, fresh_image.title)
            already_posted_list.append(fresh_image)
        gonna_post_list.clear()

        if len(already_posted_list) > 100:
            del already_posted_list[20:]
        time.sleep(3600)

except Exception as ex:
    restart()


def restart():
    import sys
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("restart now")
    import os
    os.execv(sys.executable, ['python3.5'] + sys.argv)
