from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import *
import logging
import os
import sys
from auxiliary_functions import threaded

APITOKEN = ""

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
                                                                      "your personal bot and i'm glad to start working "
                                                                      "with you.")
        username = update.message.from_user.name
        if username == TG_USERNAME:
            context.bot.send_message(chat_id=update.message.chat_id, text="Now you are allowed to talk with me. "
                                                                          "You can request your stats at any time"
                                                                          " with /stats command. Enjoy!")
        self.allowed = True
        self.myUserID = update.message.chat_id

        if not self.allowed:
            context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, you are not allowed to talk with "
                                                                          "me. Bye bye! :)")


    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


    def send_tinder_stats(self, context):

        if self.allowed:
            parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"

            if os.path.isfile(parent_folder + STATSFILE):
                statsfile = open(parent_folder + STATSFILE, "r")
                lines = statsfile.readlines()
                context.bot.send_message(chat_id=self.myUserID, text="This are your stats for today:")

                message = ''.join(lines)
                context.bot.send_message(chat_id=self.myUserID, text=message)
            else:
                context.bot.send_message(chat_id=self.myUserID, text="Today there is no statistics to show you. Sorry "
                                                                     ":(")

    def stats(self, update, context):

        if update.message.from_user.name == TG_USERNAME and self.allowed:
            self.send_tinder_stats(context)

    @threaded
    def runBot(self):

        start_handler = CommandHandler('start', self.start)
        stats_handler = CommandHandler('stats', self.stats)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(stats_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(unknown_handler)

        stats_job = self.jobqueue.run_repeating(self.send_tinder_stats, interval=60, first=0)
        self.updater.start_polling(poll_interval=0.5)
