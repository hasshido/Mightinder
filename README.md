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
  -r DISLIKER, --ratio DISLIKER		Sets the ratio of dislikes (1 is 100%)		    
  -m, --marathon	Keeps the program running and AutoLikes every 12h. 
  -b, --bot		Also starts the Telegram Bot instance
----------------------------------------------------------------------------
```

## TODO List:

### Functionalities
These are the intended next functionalities that will be included into **MighTinder**: 
 - Set dislike ratio as an argument
 - Ask for user/pass after token unsuccesful
 - Study how to implement TndrMon (Separate thread?)
	 - Improve TndrLocalizer with axis progression technique for greater precision
	 - Improve TndrLocalizer to return coordinates
	 - Improve TndrLocalizer to return coordinates over time for certain user ID
		 - Generate KML maps for Google Maps importing
 - Register match position on liking, for study purposes
	 - Seems like the matchs are always located around the third swipe:
	 - This could be "exploitable" with multiple "get nearby users" and swiping the third card
 - Telegram Bot
	 - Remote control of program execution
	 - Document the remote control capabilities
	 - Setup new matching position through attached location


### Fixes

 - Pack with Pynder modified library
	 - `User.py gives schools id error:  set generic exception catch`
 - Fix behaviour on "Bio_check" events
 	 - `print correctly on console`
 - Settings folder should be in .gitignore to avoid APIKEY leaking
	 - Also, APKIEY should be on settings folder
    
## Done
 - Auto-like stack of swipes
 - Implemented access to [Remaining Superlikes]
 - Marathon mode (sleep through swiping timeout)
 - Filters
	 - Dislike filter
	 - Superlike filter
 - Implement thread execution
	 - Execute **Telegram Bot** on another thread
		 - Show stats from current session
