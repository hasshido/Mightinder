# README

### Installation

- Install Python
- Download or clone the package.
	- Go to the program folder
	- `pip install -r requirements.txt`


### Usage


```
usage: python Mightinder.py 
		     
optional arguments: 
----------------------------------------------------------------------------
  -h, --help            Shows help message and exit
  -a, --auto            AutoLike until out of likes [default]
  -r [1-100], --ratio [1-100]		Sets the ratio of dislikes (1 is 1%)		    
  -m, --marathon	Keeps the program running and AutoLikes every 12h. 
  -b, --bot		Also starts the Telegram Bot instance
----------------------------------------------------------------------------
```

#### Telegram Bot usage
```
usage: Once core is running, Talk to him at @TheMighTinderBot

Options and commands:

 - /start
 - /help
 - /stats
 - /start_autoliker / /start_marathon / /start_tndrMon
 - /stop_autoliker / /stop_marathon / /stop_tndrMon
 - more to come ;)
```


## TODO List:

### Functionalities
These are the intended next functionalities that will be included into **MighTinder**: 

 - Ask for user/pass after token unsuccesful
 - Study how to implement TndrMon (Separate thread?)
	 - Improve TndrLocalizer with axis progression technique for greater precision
	 - Improve TndrLocalizer to return coordinates
	 - Improve TndrLocalizer to return coordinates over time for certain user ID
		 - Generate KML maps for Google Maps importing
		 - Do KML format support time as a coordinate?
 - Register match position on liking, for study purposes
	 - Seems like the matchs are always located around the third swipe:
	 - This could be "exploitable" with multiple "get nearby users" and swiping the third card
 - Telegram Bot
	 - [**Almost!**] Remote control of program execution
	 - Document the remote control capabilities
	 - Setup new matching position through attached location


### Fixes

 - Pack with Pynder modified library
	 - `User.py gives schools id error:  set generic exception catch`
 - Fix behaviour on "Bio_check" events
 	 - `print correctly on console`
    
## Done
 - Auto-like stack of swipes
 - Set dislike ratio as an argument
 - Implement access to [Remaining Superlikes]
 - Marathon mode (sleep through swiping timeout)
 - Filters
	 - Dislike filter
	 - Superlike filter
 - Implement thread execution
	 - Execute **Telegram Bot** on another thread
		 - Show stats from current session
