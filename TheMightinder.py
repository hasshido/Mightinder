import pynder
from pynder import errors
import robobrowser
import pickle
import re
import sys
import os
from random import random, randint
from time import sleep
from colorama import Fore
from auxiliary_functions import threaded, check_running, file_lock, change_running_state

# MighTinder config files
from settings import *
from sensitive_info import *


class TheMightinder:

    def __init__(self, dislike_rate=0.01):
        self.dislike_count = 0
        self.like_count = 0
        self.superlike_count = 0
        self.session = self.get_session()
        self.dislike_rate = dislike_rate

    def get_session(self):

        parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"

        try:
            # Read token
            access_token_file = open(parent_folder + "access_token.txt", "r")
            access_token = access_token_file.read()
            access_token_file.close()
            session = pynder.Session(access_token)
        except Exception:
            # Update token
            access_token = self.get_facebook_token(FACEBOOK_USER, FACEBOOK_PASSWORD, parent_folder)

            access_token_file = open(parent_folder + "access_token.txt", "w")
            access_token_file.write(access_token)
            access_token_file.close()
            session = pynder.Session(access_token)

        print(Fore.GREEN + "[OK] Session Correctly gotten")
        return session

    def get_facebook_token(self, email, password, parent_folder):

        rb = robobrowser.RoboBrowser(user_agent=MOBILE_USER_AGENT, parser="html5lib")
        
        try:
            # Read Facebook cookies
            cookies_file = open(parent_folder + "cookies.pckl", "rb")
            cookies = pickle.load(cookies_file)
            rb.session.cookies = cookies
            cookies_file.close()
            rb.open(FB_AUTH_URL)
            
        except IOError:
            # Facebook login
            rb.open(FB_AUTH_URL)
            
            login_form = rb.get_form()
            login_form["pass"] = password
            login_form["email"] = email
            rb.submit_form(login_form)

        # Get token
        auth_form = rb.get_form()
        rb.submit_form(auth_form, submit=auth_form.submit_fields["__CONFIRM__"])
        access_token = re.search(r"access_token=([\w\d]+)", rb.response.content.decode()).groups()[0]

        return access_token

    # Returns true or false (Out of likes == false)
    def check_swipes(self):
        swipes_remaining = self.session.likes_remaining
        if swipes_remaining == 0:
            return False
        return True

    def check_superswipes(self):
        return self.session._api.meta()['rating']['super_likes']['remaining']

    # Returns true or false ()
    def like_or_nope(self, user):

        action = self.check_bio(user)
        if (random() < self.dislike_rate) and action == 0:
            self.like_count += 1
            self.dislike_count += 1
            return -1
        else:
            return action

    def auto_likes(self, max_likes=25):
      
        stopper = max_likes

        if self.session:

            users = self.session.nearby_users()

            for u in users:

                if not check_running() or stopper == 0:
                    break

                try:
                    print(Fore.WHITE + '[INFO] Checking swipes remaining.')
                    status = self.check_swipes()
                    superl_status = self.check_superswipes()

                    if not status:
                        print(Fore.RED + '[ERROR] Out of swipes. Moving along...')
                        break
                    else:
                        try:
                            reaction = self.like_or_nope(u)
                            if reaction == 0:
                                u.like()
                                print(Fore.WHITE + '[INFO] Liked ' + u.name)
                                
                                stopper -= 1

                                sleep(randint(1, 2))

                            elif reaction == 1:
                                u.superlike()
                                print(Fore.WHITE + '[INFO] SuperLiked ' + u.name)
                                sleep(randint(1, 2))

                            elif reaction == -1:
                                u.dislike()
                                print(Fore.WHITE + '[INFO] Disliked ' + u.name)
                                sleep(randint(1, 2))
                        except ValueError:
                            print(Fore.RED + "[ERROR] ValueError")
                            break
                        except pynder.errors.RequestError:
                            print(Fore.RED + "[ERROR] Pynder Error. Trying to get new auth.")

                            try:
                                self.session = self.get_session()
                            except pynder.errors.RequestError:
                                print(Fore.RED + "[ERROR] Pynder Error. New auth did NOT work.")
                                break
                            continue
                        except Exception as e:
                            print(e)
                            print(Fore.RED + "[ERROR] Generic Exception. Don't know what issue is....")
                            break
                except ValueError:
                    print(Fore.RED + "[ERROR] ValueError")
                    break
                except pynder.errors.RequestError:
                    try:
                        print(Fore.RED + "[ERROR] Pynder Error. Trying to get new auth.")
                        self.session = self.get_session()
                    except pynder.errors.RequestError:
                        print(Fore.RED + "[ERROR] Pynder Error. New auth did NOT work.")
                        break
                    continue
                except Exception as e:
                    print (e)
                    print(Fore.RED + "[ERROR] Generic Exception. Don't know what issue is....")
                    break
            print(Fore.GREEN + "[OK] Session ended")
            self.show_stats()

            self.print_stats()


        else:
            print(Fore.RED + "[ERROR] Sessions is None.")

    def marathon(self):

        stop = False
        while not stop:
            try:
                self.auto_likes()
                # Tinder Default 12h (+5m) like reset for non-premium accounts.
                for i in range(1, SWIPES_REFRESH_TIMEOUT):
                    if not check_running():
                        stop = True
                        break
                    else:
                        sleep(1)

            except KeyboardInterrupt:
                print(Fore.GREEN + "[OK] Execution was interrupted by user")
                self.show_stats()
                sys.exit()

        print(Fore.GREEN + "[OK] Execution was interrupted by telegram Bot")
        self.show_stats()
        sys.exit()

    @threaded
    def start_liker(self, type, max_likes=25):
        if type == "m":
            self.marathon()
        else:
            self.auto_likes(max_likes)

        # We have finished the execution of any kind of function
        # We have to change the execution state to False
        if check_running():
            change_running_state()

    def show_stats(self):
        total_stats = self.like_count + self.dislike_count + self.superlike_count
        print(Fore.WHITE + "[INFO] Total interactions performed: " + str(total_stats))
        print(Fore.WHITE + "[INFO] Superlikes performed: " + str(self.superlike_count))
        print(Fore.WHITE + "[INFO] Likes performed: " + str(self.like_count))
        print(Fore.WHITE + "[INFO] Dislikes performed: " + str(self.dislike_count))


    def print_stats(self):

        parent_folder = os.path.dirname(os.path.realpath(sys.argv[0])) + "/"

        if os.path.isfile(parent_folder + STATSFILE):
            os.remove(parent_folder + STATSFILE)

        # Mutex to access stat file
        file_lock.acquire()
        try:
            statfile = open(STATSFILE, "w")
            total_stats = self.like_count + self.dislike_count + self.superlike_count
            statfile.write("[INFO] Total interactions performed: " + str(total_stats) + "\n")
            statfile.write("[INFO] Superlikes performed: " + str(self.superlike_count) + "\n")
            statfile.write("[INFO] Likes performed: " + str(self.like_count) + "\n")
            statfile.write("[INFO] Dislikes performed: " + str(self.dislike_count) + "\n")
            statfile.close()
        finally:
            file_lock.release()

    # Returns true or false (Blacklist on bio == hate // Lovelist on bio = love)
    def check_bio(self, user):
        if any(word in user.bio.lower() for word in BIO_BLACKLIST):
            print ("Dislike bio: " + user.bio.lower())
            self.dislike_count += 1
            return -1
        elif any(word in user.bio.lower() for word in BIO_LOVELIST) and (self.check_superswipes() > 0):
            print ("Nice bio: " + user.bio.lower())
            self.superlike_count += 1
            return 1
        else:
            self.like_count += 1
            return 0

