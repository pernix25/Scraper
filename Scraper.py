import robin_stocks.robinhood as rh
import pymysql
import pyotp
import requests
import json
import datetime
from datetime import date
import time
from option_class import *
from aws import scraper_insert

#Data storage
active_trades = []

USER = # Robinhood Username
PASS = # Robinhood Password
CODE = # Robinhood authentication code

# logs into robbinhood account
code = pyotp.TOTP(CODE).now()
rh.login(USER, PASS, mfa_code=code)

#discord channels
chanel_one = # Discord channel number

def entry_price(stock, date, strike, direction):
    """Takes a stock ticker, option date, strike price, option call or put, then returns the entry price for said option"""
    r = rh.get_option_market_data(stock, expirationDate=date, strikePrice=strike, optionType=direction)
    return float(r[0][0]['adjusted_mark_price'])

def daily_tracker(obj):
    """Gets the price for an option and appends it to the prices_per_day list in each option"""
    r = rh.get_option_market_data(obj._stock, expirationDate=obj._option_date, strikePrice=obj._strike, optionType=obj._direction)
    obj.prices_per_day.append(r[0][0]['adjusted_mark_price'])

def min_max(obj):
    """Takes an option object and returns a tuple of the min and max for all values in the prices_per_day"""
    """Also takes replaces the objects all time min max with the new all time min/max"""
    opt_max = 0.00
    opt_min = 1000.00
    for lyst in obj.prices_per_week:
        if max(lyst) > opt_max:
            opt_max = max(lyst)
        if min(lyst) < opt_min:
            opt_min = min(lyst)
    obj.daily_min_maxes[len(obj.daily_min_maxes)] = (opt_min, opt_max)

    if opt_min < obj.all_time_min_max[0] and opt_max > obj.all_time_min_max[1]:
        obj.all_time_min_max = (opt_min, opt_max)
    elif opt_min < obj.all_time_min_max[0]:
        obj.all_time_min_max = (opt_min, obj.all_time_min_max[1])
    elif opt_max > obj.all_time_min_max[1]:
        obj.all_time_min_max = (obj.all_time_min_max[0], opt_max)

def rm_exp_opt():
    """removes options in active_trades based on expiration options expiration date"""
    for option in active_trades:
        if option._exp_date < str(date.today()):
            active_trades.remove(option)

def retrieve_messages(channel_id):
    """Discord webscraper - input a discord channel number to scrape messages"""
    headers = {
        'authorization': # Discord authorization code
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages', headers = headers)
    scraper = json.loads(r.text)
    for value in scraper:
        content = value['content']
        timestamp = value['timestamp'][:10]
        if (*) in content and timestamp == str(date.today()): # (*) = keyword for buying option such as 'bought', 'in', 'buying', 'buy'
            content = str(content)
            content = content.split()
            if len(content) == 5 or len(content) == 6: # caters to messages that are information specific like (bought telsa 300 calls 2/25)
                stock = content[1].upper() 
                strike = content[2]
                direction = content[3]
                if direction == 'calls': # changes option type to format that works with robinhood api
                    direction = 'call'
                elif direction == 'puts':
                    direction = 'put'
                option_date = content[4]
                if len(option_date) == 3 or len(option_date) == 4 or len(option_date) == 5: # changes option date to format that works with robinhood api
                    option_date = option_date + '/2023'
                option_date = datetime.datetime.strptime(option_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                today = date.today()
                if option_date < str(today): # checks for old options and discrads them
                    print('EXPIRED OPTION')
                else:
                    x = Option(stock, int(strike), direction, option_date)
                    duplicate = True
                    if len(active_trades) == 0:
                        x.entry_price = entry_price(x._stock, x._option_date, x._strike, x._direction)
                        active_trades.append(x) # apends option to active_trades to manage active options
                        scraper_insert('February', x._stock, x._strike, x._direction, x._option_date, x.entry_price) #adds option to aws database
                    else: # prevents duplicate options
                        for obj in active_trades:
                            if x.is_same_as(obj):
                                duplicate = False
                        if duplicate:
                            x.entry_price = entry_price(x._stock, x._option_date, x._strike, x._direction)
                            active_trades.append(x)
                            scraper_insert('February', x._stock, x._strike, x._direction, x._option_date, x.entry_price)

def main():
    
    while True:
        ts = str(datetime.datetime.now())[11:16]
        if ts == '06:00':
            rm_exp_opt() # removes expired options in active trades list 
        elif ts <= '07:29':
            print('Market is not open')
            time.sleep(60)
        elif ts >= '07:30' and ts <= '13:59':
            retrieve_messages(chanel_one)
            if len(active_trades) >= 1:
                for obj in active_trades: # need to add multi proccessing/threading branch to run more efficiently
                    daily_tracker(obj)
            time.sleep(5)
        elif ts == '14:00':
            for obj in active_trades:
                # finds min/max option price and appends daily lists to weeklies inside each option object
                min_max(obj)
                obj.end_day()
        elif ts >= '14:01':
            print('Market is closed')
            time.sleep(60)
        else:
            print('Error')
            time.sleep(60)

if __name__ == "__main__":
    main()
