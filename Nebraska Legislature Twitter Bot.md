# Nebraska Legislature Twitter Bot

*Last updated: Feb. 17, 2017*

This bot looks through the [daily summary sheet](http://nebraskalegislature.gov/calendar/summary.php?day=2017-02-16) to find bills and resolutions that have been adopted, passed or approved by the governor. It runs every 15 minutes between 9 a.m. and 5 p.m., Monday through Friday.

The bot keeps track of past tweets by writing them to a text file. Before sending a tweet, it checks the text file (billsbot.txt) to see if it has been tweeted before. This prevents the bot from tweeting the same tweet multiple times.

The Twitter account is [@NeLegBills](http://twitter.com/nelegbills).

