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


L.login(USER , PASSWORD)
print('Successfully Logged in to profile:' , USER ,'!')



@bot.message_handler(regexp="")
def linkto(message):
    urldetail = (message.text).split('/')
    if 'p' in urldetail:
        url_index = urldetail.index('p')
    elif 'tv' in urldetail:
        url_index = urldetail.index('tv')
    url = urldetail[int(url_index)+1]
    bot.send_message(message.chat.id,'Please, wait a few minutes! Your post is downloading!')
    post  = instaloader.Post.from_shortcode(L.context, url)
    L.download_post(post,target="posts")


    files_path = os.path.join('posts', '*.jpg')
    files_path2 = os.path.join('posts', '*.mp4')
    files_path3 = os.path.join('posts', '*.txt')
    if files_path:
        files = sorted(
            glob.iglob(files_path), key=os.path.getctime, reverse=True) 
        files3 = sorted(
            glob.iglob(files_path3), key=os.path.getctime, reverse=True) 
        print(files[0])
        f = open(f"{files[0]}", "rb")
        txt="hello"

        bot.send_photo(message.chat.id,f,caption=txt+"\n\nDownloaded by @instasave_new_bot")
    if files_path2:
        files = sorted(
        glob.iglob(files_path2), key=os.path.getctime, reverse=True) 
        files3 = sorted(
            glob.iglob(files_path3), key=os.path.getctime, reverse=True) 
        print(files[0])
        f = open(f"{files[0]}", "rb")
        txt="hello"

        bot.send_video(message.chat.id,f,caption=txt+"\n\nDownloaded by @instasave_new_bot")
        
    time.sleep(2)
    files = glob.glob('posts/*')
    for f in files:
        os.remove(f)



bot.infinity_polling()