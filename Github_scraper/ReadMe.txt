How to use:
1.  run sqlite_creation.py
2.  either set discord server in Scraper.py or enter discord server id as an argument on commandline (buy indicator may change from server to server)

Main file: Scraper.py
    This script will scrape a discord server to purchase/sell stock options as well as upload the option information to a sqlite database.

sqlite_creation.py:
    Creates the sqlite database used for Scraper.py

login_info.txt:
    Stores all sensitive information such as usernames and passwords to login into robinhood and discord.
    This file will be read by Scraper.py with each line storing a username, password, or authorization code

option.py:
    Option class

ERD_Scraper.pdf:
    Sqlite database ERD

discord_data:
    Sample data scraped from discord used to evaluate how main script will purchase and sell stock options
