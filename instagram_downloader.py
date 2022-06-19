from datetime import datetime
import requests
import re
import time
import telebot
import flask
import glob
import os
from pathlib import Path
from tqdm import tqdm
import logging
import time
API_TOKEN = '5528813146:AAHtgSpySLIp-8Av6LNGQpnVx4iLvs3-Yu4'

bot = telebot.TeleBot(API_TOKEN)


WEBHOOK_HOST = 'instauzbek.herokuapp.com'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.get('/')
def index():
    bot.remove_webhook()

    time.sleep(0.1)

    # Set webhook
    bot.set_webhook(url=WEBHOOK_HOST + WEBHOOK_URL_PATH,
                )
    import instaloader

    L = instaloader.Instaloader()


    USER = "fastlogzapp"


    PASSWORD = "asaka.uz1"
    L.login(USER , PASSWORD)
    print('Successfully Logged in to profile:' , USER ,'!')
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)



group_id = '-1001600708495'





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
        
# Remove webhook, it fails sometimes the set if there is a previous webhook


# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        debug=True)