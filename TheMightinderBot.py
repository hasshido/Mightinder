import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os, sys

# MighTinder config files
from settings import *
from sensitive_info import *
from auxiliary_functions import threaded, check_running, change_running_state, file_lock
from TheMightinder import TheMightinder




class TheMightinderBot:

    def __init__(self):
        self.updater = Updater(token=APITOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.jobqueue = self.updater.job_queue
        self.myUserID = 0
        self.allowed = False

    def start(self, update, context):
        """
        This function implements the bot's start functionality. It allows a predefined user to interact with TheMightinderBot
        :param update: The recieved object
        :param context: The context of message
        :return: none
        """
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


    def stop(self, update, context):
        """
        This function implements the stop bot command. It checks if TheAlmightinder instance is running and stops any
        kind of execution.
        :param update: The recieved object
        :param context: The context of message
        :return: none
        """
        if update.message.from_user.name == TG_USERNAME and self.allowed:
            if not check_running():
                context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, <i>TheMightinder</i> is not running at "
                                                                              "this time.\nIf you want to start some "
                                                                              "functionality, please type /help to "
                                                                              "view available commands.",
                                         parse_mode=telegram.ParseMode.HTML)

            else:
                change_running_state(False)

            context.bot.send_message(chat_id=update.message.chat_id, text="Done!\nYour tinder autolike has started.\n"
                                                                          "Good luck!")

        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING)


    def send_tinder_stats(self, context):
        """
        This function implements the bot's stat reporting functionality
        :param context: The context of message
        :return: none
        """
        if self.allowed:
            parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"

            if os.path.isfile(parent_folder + STATSFILE):

                # Mutex to access stats file
                file_lock.acquire()
                try:
                    statsfile = open(parent_folder + STATSFILE, "r")
                    lines = statsfile.readlines()
                    message = ''.join(lines)
                    context.bot.send_message(chat_id=self.myUserID, text="These are your stats for the last session:\n"
                                                                         + message)
                finally:
                    file_lock.release()

            else:
                context.bot.send_message(chat_id=self.myUserID, text="There are no statistics to show you yet.\n"
                                                                     "Come back later :)")

    def stats(self, update, context):
        """
        This function implements a wrapper to execute stats reporting
        :param update: The recieved object
        :param context: The context of message
        :return: none
        """
        if update.message.from_user.name == TG_USERNAME and self.allowed:
            self.send_tinder_stats(context)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING)


    def help(self, update, context):

        """
        Just shows Help on chat
        :param update: The recieved object
        :param context: The context of message
        :return: none
        """       
        if update.message.from_user.name == TG_USERNAME and self.allowed:

            context.bot.send_message(chat_id=update.message.chat_id, text=HELPSTRING)

        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING)

    def start_autolike(self, update, context):
        """
        This function implements the start_autolike bot command. It checks if TheAlmightinder instance is running and,
        if not, it runs marathon thread
        :param update: The recieved object
        :param context: The context of message
        :return: none
        """
        if update.message.from_user.name == TG_USERNAME and self.allowed:
            if check_running():
                context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, <i>TheMightinder</i> is already "
                                                                              "running.\nIf you want to restart it, "
                                                                              "please type /stop and then "
                                                                              "/start_autolike.")

            else:
                change_running_state(True)
                theMightinder = TheMightinder()
                theMightinder.start_liker("a")
                context.bot.send_message(chat_id=update.message.chat_id, text="Done!\nYour tinder autolike has started.\n"
                                                                            "Good luck!")
                change_running_state(False)
        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING)


    def start_marathon(self, update, context):
        """
        This function implements the start_marathond bot command. It checks if TheAlmightinder instance is running and,
        if not, it runs marathon thread
        :param update: The recieved object
        :param context: The context of message
        :return: none
        """
        if update.message.from_user.name == TG_USERNAME and self.allowed:
            if check_running():
                context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, <i>TheMightinder</i> is already "
                                                                              "running.\nIf you want to restart it, "
                                                                              "please type /stop and then "
                                                                              "/start_marathon.",
                                         parse_mode=telegram.ParseMode.HTML)

            else:
                change_running_state(True)
                theMightinder = TheMightinder()
                theMightinder.start_liker("m")

            context.bot.send_message(chat_id=update.message.chat_id, text="Done!\nYour tinder marathon has started.\n"
                                                                          "Good luck!")

        else:
            context.bot.send_message(chat_id=update.message.chat_id, text=NOT_AUTH_STRING)

    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


    def runBot(self):

        start_handler = CommandHandler('start', self.start)
        stats_handler = CommandHandler('stats', self.stats)
        st_autolike_handler = CommandHandler('start_autolike', self.start_autolike)
        st_marathon_handler = CommandHandler('start_marathon', self.start_marathon)
        stop_handler = CommandHandler('stop', self.stop)
        help_handler = CommandHandler('help', self.help)
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(st_autolike_handler)
        self.dispatcher.add_handler(st_marathon_handler)
        self.dispatcher.add_handler(stats_handler)
        self.dispatcher.add_handler(stop_handler)
        self.dispatcher.add_handler(help_handler)

        unknown_handler = MessageHandler(Filters.command, self.unknown)
        self.dispatcher.add_handler(unknown_handler)

        stats_job = self.jobqueue.run_repeating(self.send_tinder_stats, interval=60, first=0)
        self.updater.start_polling(poll_interval=0.5)
