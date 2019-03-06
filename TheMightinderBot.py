from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os, sys

# MighTinder config files
from settings import *
from sensitive_info import *




class TheMightinderBot:

    def __init__(self):
        self.updater = Updater(token=APITOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.jobqueue = self.updater.job_queue
        self.myUserID = 0
        self.allowed = False
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)


    def start(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to TheAlmightinder reporting system! Im "
                                                                      "your personal bot and I'm glad to start working "
                                                                      "with you.")
        username = update.message.from_user.name
        self.myUserID = update.message.chat_id

        if username == TG_USERNAME:
            self.allowed = True
            context.bot.send_message(chat_id=update.message.chat_id, text="Now you are allowed to talk with me.\n\r"
                                                                          "Use /help to show available options. "
                                                                          "Enjoy!")
           
        if not self.allowed:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING)


    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def help(self, update, context):
        if self.allowed:
            context.bot.send_message(chat_id=update.message.chat_id, text=HELPSTRING)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING) 


    def send_tinder_stats(self, context):

        
        parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"

        if self.allowed:
            if os.path.isfile(parent_folder + STATSFILE):
                statsfile = open(parent_folder + STATSFILE, "r")
                lines = statsfile.readlines()
                context.bot.send_message(chat_id=self.myUserID, text="These are your stats for today:")

                message = ''.join(lines)
                context.bot.send_message(chat_id=self.myUserID, text=message)
            else:
                context.bot.send_message(chat_id=self.myUserID, text="Today there are no statistics to show for you. Sorry "
                                                                        ":(")
        else:
            context.bot.send_message(chat_id=self.myUserID, text=NOT_AUTH_STRING) 

    def stats(self, update, context):

        if update.message.from_user.name == TG_USERNAME and self.allowed:
            self.send_tinder_stats(context)


    def runBot(self):

        start_handler = CommandHandler('start', self.start)
        stats_handler = CommandHandler('stats', self.stats)
        help_handler = CommandHandler('help', self.help)
        unknown_handler = MessageHandler(Filters.command, self.unknown)

        self.dispatcher.add_handler(start_handler)     
        self.dispatcher.add_handler(stats_handler)
        self.dispatcher.add_handler(help_handler)
        self.dispatcher.add_handler(unknown_handler)

        stats_job = self.jobqueue.run_repeating(self.send_tinder_stats, interval=60, first=0)

        self.updater.start_polling(poll_interval=0.5)


if __name__ == "__main__":
    bot = TheMightinderBot()
    bot.runBot()
