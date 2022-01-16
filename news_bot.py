# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 12:04:46 2022

@author: laksh
"""
"""
References : 1. https://python-telegram-bot.readthedocs.io/en/stable/  go to this link for referring the func usage
"""
import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext, Dispatcher
from telegram import Update,Bot,ReplyKeyboardMarkup
from flask import Flask, request

 #logging: any kind of error happen or warning is raised, so this is used to parse it in a systematic manner 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 	                level=logging.INFO)
#logger object can create logs for your program
logger=logging.getLogger(__name__)
 
TOKEN ="5083717400:AAGiI5biR7kXaKm07xejpu-WceD1aZ6vIvI" # A token of newsExtractor telegram bot
topics_keyboard = [
    ['Top Stories', 'World', 'Nation'], 
    ['Business', 'Technology', 'Entertainment'], 
    ['Sports', 'Science', 'Health']
]

##### Flask part  ########
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello! We are using ngrok server"

@app.route(f'/{TOKEN}', methods=['GET', 'POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dp.process_update(update)
    return "ok"
## -----------------------------------------------------------------------

### Main Functions #################
def greeting(update: Update,context: CallbackContext):
    print(update)
    first_name = update.to_dict()['message']['chat']['first_name']
##    print(update.to_dict().keys(),first_name)
    update.message.reply_text("Hi {}. Dear have a nice day".format(first_name))
    
def _help(update: Update,context: CallbackContext):
    help_txt = "In case of query contact 9911****."
    update.message.reply_text(help_txt)

def echo_text(update: Update,context: CallbackContext):
    text = update.to_dict()['message']['text']
    update.message.reply_text(text)


def echo_sticker(update: Update, context: CallbackContext):
    update.message.reply_sticker(sticker=update.message.sticker.file_id)

def error(bot,update):
    logger.error("Update '%s' has caused error '%s", update, update.error)#update.error contains error if caused due to update.

def news_topics(update: Update, context: CallbackContext):
    update.message.reply_text(text="Choose a category",
                     reply_markup = ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))

## --------------------------------------------------------
# def main():
if __name__=="__main__":
    bot = Bot(TOKEN)
    # updater=Updater(TOKEN)  # updater will keep polling and receive the updates from telegram and move it to the dispatcher
    bot.set_webhook("https://fierce-shore-54570.herokuapp.com/"+ TOKEN)   #URL of port 8443 created by ngrok, now we are not using telegram server
    dp = Dispatcher(bot, None)
    
    
    #Add handlers
    #dispatcher needs multiple handlers
    #former start is for: if the user writes / with start then it will call the start(latter) function
    dp.add_handler(CommandHandler("start" , greeting))
    dp.add_handler(CommandHandler("help" , _help))
    dp.add_handler(CommandHandler("news_topics" , news_topics))
    
    #messageHandler class is for handling stickers and other text and if the msg is in text form user .text
    dp.add_handler(MessageHandler(Filters.text , echo_text))
    dp.add_handler(MessageHandler(Filters.sticker ,echo_sticker))
    dp.add_error_handler(error)
    
    app.run(port=8443)

"""
from gnewsclient import gnewsclient

client = gnewsclient.NewsClient()

#See the default configurations
print(client.get_config())

#>>> {'location': 'United States', 'language': 'english', 'topic': 'Top Stories'}

#Default topics
print(client.topics)
# >>> ['Top Stories', 'World', 'Nation', 'Business', 'Technology', 'Entertainment', 'Sports', 'Science', 'Health']


# Updating some default value
client.location = 'India'
client.language = 'Hindi'
client.topic = 'Sports'

# to gets news urls 
print(client.get_news())

# >>> [
     {'title': 'South Africa vs India: विराट कोहली का छलका दर्द, बोले बल्लेबाजों की नाकामी पर कोई बहाना नही - Navbharat Times', 
      'link': 'https://news.google.com/__i/rss/rd/articles/CBMivAFodHRwczovL25hdmJoYXJhdHRpbWVzLmluZGlhdGltZXMuY29tL3Nwb3J0cy9jcmlja2V0L2luZGlhLWluLXNvdXRoLWFmcmljYS92aXJhdC1rb2hsaS1ub3QtaGFwcHktd2l0aC1iYXR0ZXJzLWFmdGVyLWluZGlhLWxvc3QtdGhlLXRlc3Qtc2VyaWVzLWFnYWluc3Qtc291dGgtYWZyaWNhL2FydGljbGVzaG93Lzg4ODk5Njk5LmNtc9IBAA?oc=5', 
      'media': None}, 
     {'title': 'Ind vs SA 3rd Test: केप टाउन टेस्ट हार टूटा भारत का द. अफ्रीका में पहली टेस्ट सीरीज जीतने का सपना - Hindustan', 
      'link': 'https://news.google.com/__i/rss/rd/articles/CBMipgFodHRwczovL3d3dy5saXZlaGluZHVzdGFuLmNvbS9jcmlja2V0L3N0b3J5LWluZGlhLXZzLXNvdXRoLWFmcmljYS0zcmQtdGVzdC1kYXktNGEtbWF0Y2gtcmVwb3J0LWluZC12cy1zYS0zcmQtdGVzdC1saXZlLXNjb3JlLXVwZGF0ZXMtYW5kLWhpbmRpLWNvbW1lbnRhcnktNTU3MjEzOC5odG1s0gEA?oc=5', 
      'media': None}, ...]

"""