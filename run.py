from TheMightinderBot import TheMightinderBot
from TheMightinder import TheMightinder
from auxiliary_functions import check_positive, set_running_state
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auto", help="AutoLike until out of likes [default]", action="store_true")
    parser.add_argument("-r", "--ratio", type=check_positive, default=1, help="Percentage dislake_rate. If not "
                                                                                 "set, is always 1%")
    parser.add_argument("-m", "--marathon", help="Keeps the program running and AutoLikes every 12h. Ideal for AFK "
                                                 "Farming.", action="store_true")
    parser.add_argument("-b", "--bot", help="Starts the Tinder bot TheMightinderBot for Telegram", action="store_true")
    args = parser.parse_args()
    args_dict = vars(args)
    n_args_not_empty = sum(1 for arg_value in args_dict.values() if arg_value)

    if args.marathon and args.auto:
        raise argparse.ArgumentTypeError("Invalid configuration. You have selected both -m and -a. Select just one.")

    # dislake_rate. If not set, is allways 0.01
    dislike_ratio = float(args.ratio / 100)

    theMightinder = TheMightinder(dislike_ratio)
    theMightinderBot = TheMightinderBot()

    set_running_state(True)

    if args.bot:
        theMightinderBot.runBot()

    if n_args_not_empty == 1 or args.auto:
        theMightinder.start_liker("a", max_likes=1)

    elif args.marathon:
        theMightinder.start_liker("m")




