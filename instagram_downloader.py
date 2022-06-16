from datetime import datetime
import requests
import re
import time
import telebot

import glob
import os
from instabot import Bot
from pathlib import Path
from tqdm import tqdm

token = '5528813146:AAHtgSpySLIp-8Av6LNGQpnVx4iLvs3-Yu4'
bot = telebot.TeleBot(token)


import instaloader

L = instaloader.Instaloader()


USER = "fastlogzapp"


PASSWORD = "asaka.uz1"

group_id = '-1001600708495'

L.login(USER , PASSWORD)
print('Successfully Logged in to profile:' , USER ,'!')

@bot.message_handler(commands=['start'])
def start(message):
    f_read = open("podpis.txt","r")
    f1 = f_read.readlines()
    if str(message.chat.id)+'\n' in f1:
        pass
    else:
        f = open("podpis.txt","a+")
        f.write(f"{message.chat.id}\n")
        f.close()
        bot.send_message(group_id,f"{message.chat.id}, @{message.chat.username if message.chat.username else 'no username'}")
    bot.send_message(message.chat.id,"Please, send a link! I'm ready to download it!😎")
@bot.message_handler()
def linkto(message):
    if (message.text).startswith('https://www.instagram.com'):
        try: 
            urldetail = (message.text).split('/')
            if 'p' in urldetail:
                url_index = urldetail.index('p')
            elif 'tv' in urldetail:
                url_index = urldetail.index('tv')
            elif 'reel' in urldetail:
                url_index = urldetail.index('reel')
            url = urldetail[int(url_index)+1]
            bbbb = bot.send_message(message.chat.id,'Please, wait a few seconds! Your post is downloading!😊')
            post  = instaloader.Post.from_shortcode(L.context, url)
            L.download_post(post,target="posts")


            files_path = os.path.join('posts', '*.jpg')
            files_path2 = os.path.join('posts', '*.mp4')
            files_path3 = os.path.join('posts', '*.txt')
            if files_path and files_path2 == None:
                files = sorted(
                    glob.iglob(files_path), key=os.path.getctime, reverse=True) 
                files3 = sorted(
                    glob.iglob(files_path3), key=os.path.getctime, reverse=True) 
                print(files[0])
                f = open(f"{files[0]}", "rb")
                txt=""

                bot.send_photo(message.chat.id,f,caption=txt+"\n\nDownloaded by @instasave_new_bot")
            if files_path2:
                files = sorted(
                glob.iglob(files_path2), key=os.path.getctime, reverse=True) 
                files3 = sorted(
                    glob.iglob(files_path3), key=os.path.getctime, reverse=True) 
                print(files[0])
                f = open(f"{files[0]}", "rb")
                txt=""

                bot.send_video(message.chat.id,f,caption=txt+"\n\nDownloaded by @instasave_new_bot")
                
            time.sleep(3)
            files = glob.glob('posts/*')
            for f in files:
                os.remove(f)
            bot.delete_message(message.chat.id,bbbb.id)
        except:
            bot.send_message(message.chat.id,'Too many requests! Please try again few seconds later!😊')

    else:
        bot.send_message(message.chat.id,'Send only Instagram links!')
        
bot.infinity_polling()