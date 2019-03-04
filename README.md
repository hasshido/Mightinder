
# README


### Use:

Just install requirements.txt, and call the script as follows:

```
usage: Mightinder.py [-h] [-a] [-r DISLIKER]

optional arguments:
  -h, --help            show this help message and exit
  -a, --auto            AutoLike until out of likes [default]
  -r DISLIKER, --disliker DISLIKER
                        Percentage dislike ratio

```

### TODO List:
 
1. Check if >25 likes on one sitting works correctly
2. Auto: Ask for Dislike ratio

3. Auto: Ask for user/pass after token unsuccesful
4. Auto: Ask for Sleep for 12:10h after ending
5. Filter: Add filtering blacklist

6. Modify Requisites.txt to add versions
7. Pack with Pynder modified library (user.py with generic exception catch)

8. Add TndrLocalizer to main loop
    - Improve TndrLocalizer to show one point
		- Give google maps info for that location
	- Add TndrLocalizer over time

9. Register match position on liking 

10. Auto: Telegram Summary with new matches
    1.  [In Progress] Summary with new matches
    2.  Remote control
    3.  Modify location using "current location"
    
11. Change functionality to implement thread execution
    - DONE