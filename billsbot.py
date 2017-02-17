import requests, os, smtplib
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
from twython import Twython

# The process is enclosed in a try block. If an error occurs, it send an email with the error message.
try:
    # This creates a twitter variable using the Twitter account's API keys and access tokens. Go to apps.twitter.com to find those values for your account.
    API_KEY = ''
    API_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''
    twitter = Twython(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # This gets today's date and formats it as "YYYY-MM-DD" to create an updated url for each day.
    today = date.today()
    date = today.strftime("%Y-%m-%d")
    url = "http://nebraskalegislature.gov/calendar/summary.php?day=" + date

    # Here, we get the path to the script so it can find the text file in the same directory. Then, we open the file and read the lines into a list.
    directory = os.path.dirname(__file__)
    filename = "billsbot.txt"
    filepath = os.path.join(directory, filename)
    past = open(filepath, 'r+')
    lines = past.readlines()

    # This gets the data from the summary sheet website and loads it as a BeautifulSoup object.
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html5lib')

    # This finds the table of entries and loads the rows into a list.
    table = soup.find('tbody')
    rows = table.find_all('tr')

    # Then, it loops through the rows and gets the information about each entry.
    for row in rows:
        cells = row.find_all('td')
        number = cells[0].text.strip()
        url = cells[0].find('a')['href']
        link = "http://nebraskalegislature.gov/" + url
        description = cells[1].text.strip()
        page = cells[2].text.strip()
        # If the entry description starts with "Passed on Final Reading," "Approved by Governor" or just says "Adopted," it creates a tweet. If the tweet is too long, it truncates it and adds an ellipsis. Then, it checks to see if the tweet has already been tweeted. If not, it tweets it and writes it to the file. The filetweet allows the tweets to be written on new lines without tweeting the newline character.
        if description[:23] == "Passed on Final Reading":
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, 'html5lib')
            name = soup.find('h2').text.strip()
            if len(name) > 98:
                name = name[:95] + "..."
            tweet = "PASSED: " + name + " #neleg dataomaha.com/legislature/bills/" + number
            filetweet = tweet + '\n'
            if filetweet not in lines: 
                print(tweet)
                past.write(filetweet)
                twitter.update_status(status=tweet)
        elif description[:20] == "Approved by Governor":
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, 'html5lib')
            name = soup.find('h2').text.strip()
            if len(name) > 88:
                name = name[:85] + "..."
            tweet = "APPROVED BY GOV.: " + name + " #neleg dataomaha.com/legislature/bills/" + number
            filetweet = tweet + '\n'
            if filetweet not in lines: 
                print(tweet)
                past.write(filetweet)
                #twitter.update_status(status=tweet)
        elif description == "Adopted":
            r = requests.get(link)
            data = r.text
            soup = BeautifulSoup(data, 'html5lib')
            name = soup.find('h2').text.strip()
            if len(name) > 97:
                name = name[:94] + "..."
            tweet = "ADOPTED: " + name + " #neleg dataomaha.com/legislature/bills/" + number
            filetweet = tweet + '\n'
            if filetweet not in lines: 
                print(tweet)
                past.write(filetweet)
                twitter.update_status(status=tweet)
        print(number)
except BaseException as e:
    # If an error is raised, it sends the error message in an email.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("SenderEmailAddress", "SenderEmailPassword")
    
    msg = "Bot failed: " + str(e)
    server.sendmail("SenderEmailAddress", "RecipientEmailAddress", msg)
    server.quit()
        