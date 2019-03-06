SWIPES_REFRESH_TIMEOUT = 43500

MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; U; en-gb; KFTHWI Build/JDQ39) AppleWebKit/535.19 (KHTML, like Gecko) " \
                    "Silk/3.16 Safari/535.19 "
FB_AUTH_URL = "https://www.facebook.com/v2.6/dialog/oauth?redirect_uri=fb464891386855067%3A%2F%2Fauthorize%2F&display" \
              "=touch&state=%7B%22challenge%22%3A%22IUUkEUqIGud332lfu%252BMJhxL4Wlc%253D%22%2C%220_auth_logger_id%22" \
              "%3A%2230F06532-A1B9-4B10-BB28-B29956C71AB1%22%2C%22com.facebook.sdk_client_state%22%3Atrue%2C" \
              "%223_method%22%3A%22sfvc_auth%22%7D&scope=user_birthday%2Cuser_photos%2Cuser_education_history%2Cemail" \
              "%2Cuser_relationship_details%2Cuser_friends%2Cuser_work_history%2Cuser_likes&response_type=token" \
              "%2Csigned_request&default_audience=friends&return_scopes=true&auth_type=rerequest&client_id" \
              "=464891386855067&ret=login&sdk=ios&logger_id=30F06532-A1B9-4B10-BB28-B29956C71AB1&ext=1470840777&hash" \
              "=AeZqkIcf-NEW6vBd "

STATSFILE = "stats.txt"
HELPSTRING = "This is TheMightinderBot help.\n" + \
            "**Available commands:**\n" + \
            "/start - Starts bot functionality and checks username\n" + \
            "/stop - Stops all kind of execution\n" + \
            "/stats - Gets last session Tinder stats of current user\n" + \
            "/start_autolike - Starts one iteration of the auto-liker\n" + \
            "/start_marathon - Starts a continue execution of the auto-liker\n" + \
            "/help - Shows this message"
NOT_AUTH_STRING = "Sorry, you are not allowed to talk with me. Please use /start to authenticate first"
STATS_HOURS_INTERVAL = 1440 # 60m * 24h

