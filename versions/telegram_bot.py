# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 12:04:46 2022

@author: laksh
"""

import logging
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters,CallbackContext
 #Enable logging
from telegram import Update,Bot,ReplyKeyboardMarkup

 #logging: any kind of error happen or warning is raised, so this is used to parse it in a systematic manner 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 	                level=logging.INFO)
#logger object can create logs for your program
logger=logging.getLogger(__name__)
 
TOKEN ="5083717400:xyz-WceD1aZ6vIvI"
#https://python-telegram-bot.readthedocs.io/en/stable/ go to this link for referring the func usage

topics_keyboard = [
    ['Top Stories', 'World', 'Nation'], 
    ['Business', 'Technology', 'Entertainment'], 
    ['Sports', 'Science', 'Health']
]

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

def main():
    updater=Updater(TOKEN)#updator will keep polling and receive the updates from telegram and move it to the dispatcher
    #dispatcher handles those updates
    dp=updater.dispatcher #all the response will be handled

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

    updater.start_polling()
    logger.info("Started polling...")
    updater.idle()#waits until the user presses ctrl+c or anything to stop the program

if __name__=="__main__":
    main()