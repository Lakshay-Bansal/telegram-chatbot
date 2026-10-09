# -*- coding: utf-8 -*-
"""
Created on Thu Jan 13 21:17:57 2022

@author: laksh
"""
## My telegram bot name is newsExtracter
# username of bot is newsLaksh_bot
# This code is simple a echo bot

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# enable looging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "5083717400:xyz-WceD1aZ6vIvI"


def start(bot, update):
    print(update)
    author = update.message.from_user.first_name
    # msg = update.message.text
    reply = "Hi {}".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)
    
def _help(bot, update):
    help_txt = "In case of query contact 9911****."
    bot.send_message(chat_id=update.message.chat_id, text= help_txt)
    
def echo_text(bot, update):
    reply = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text=reply)

def echo_sticker(bot, update):
    #To send the same message received from the user
    bot.send_sticker(chat_id = update.message.chat_id, 
                     sticker = update.message.sticker.file_id)

def error(bot, update):
    logger.error("Update '%s' caused error '%s'", update, update.error)
    
    
def main():
    updater = Updater(TOKEN)
    
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", _help))
    dp.add_handler(MessageHandler(Filters.text, echo_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    
    dp.add_error_handler(error)
    
    updater.start_polling()
    logger.info("Started Polling...")
    updater.idle()  #To stop the program by pressing ctrl + C

if __name__ == "__main__":
    main()