import numpy as np
import sqlite3 as sql
import robin_stocks.robinhood as rh
import json
import requests
from datetime import date, datetime
import time
from option import Option
import pyotp
import sys

# gets sensitive login information stored in seperate txt file
with open("login_info.txt", 'r') as r_info:
    lines = r_info.readlines()
    USER = lines[0].strip()
    PASSW = lines[1].strip()
    CODE = lines[2].strip()
    DISCORD_AUTHORIZATION = lines[3].strip()

# logins to robinhood account
code = pyotp.TOTP(CODE).now()
rh.login(USER,PASSW, mfa_code=code)

# connects to sqlite database
conn = sql.connect('Scraper.db')
cur = conn.cursor()

# Discord Channels
if len(sys.argv) > 1:
    primary = str(sys.argv[1])
else:
    print('Either set primary to discord server id or enter it as a commandline arg')

# --- functions --- 
def upload_option(opt):
    cur.execute(f"INSERT INTO ActiveOptions (option_id) VALUES (?)", (opt.option_id,))
    conn.commit()

def get_day_trades() -> bool:
    day_trades = rh.account.get_day_trades()
    num_day_trades = len(day_trades["equity_day_trades"]) + len(day_trades["option_day_trades"])
    if num_day_trades < 3:
        return True
    else:
        return False
    
def get_open_positions():
    return rh.options.get_open_option_positions()

def get_buying_power():
    return float(rh.load_account_profile()['buying_power'])

def get_active_options():
    # retrieves all active options from db and instantiates them into a list of Option objects
    result = []
    cur.execute(f"SELECT Stocks.ticker_desc, Options.strike, Options.exp_date, OptTypes.type_desc, Options.option_id, Options.opt_desc FROM Options INNER JOIN Stocks ON Options.ticker_id = Stocks.ticker_id INNER JOIN OptTypes ON Options.type_id = OptTypes.type_id WHERE Options.option_id IN (SELECT * FROM ActiveOptions)")
    db_data = cur.fetchall()

    for data in db_data:
        result.append(Option(data[0], str(data[1]), data[2], data[3], data[-1], data[-2], False, False))
    
    return result

def get_prices(option_list):
    # uploads prices of active options to db
    for option in option_list:
        price = option.get_curr_price()
        cur.execute(f"INSERT INTO Prices (option_id, price, tmstp) VALUES (?,?,?)", (option.option_id, price, str(datetime.now())[:18]))
        conn.commit()

def scrape(day, option_list):
    # gets messages from discord channel
    headers = {
        'authorization': DISCORD_AUTHORIZATION
    }
    r = requests.get(f'https://discord.com/api/v9/channels/{primary}/messages', headers = headers)
    scraper = json.loads(r.text)

    for text in scraper:
        # skips current message if posted on a previous day
        if text['timestamp'][:10] != day:
            continue
        else:
            lyst = text['content'].split('\n')
            for item in lyst:
                item = item.split(' ')
                if 'BOUGHT' in item:
                    stock = item[1]
                    opt_date = datetime.strptime((item[2] + '/2023'), '%m/%d/%Y').strftime('%Y-%m-%d')
                    strike = item[3][:-1]
                    if item[3][-1] == 'C':
                        opt_type = 'call'
                    elif item[3][-1] == 'P':
                        opt_type = 'put'
                    else:
                        continue

                    if 'lotto' in item:
                        # record lotto trade, but do not purchase
                        option_list.append(Option(stock, strike, opt_date, opt_type, opt_desc='lotto'))
                    else:
                        # checks if option is day trade-able
                        day_trades = rh.get_day_trades()
                        num_day_trades = len(day_trades["equity_day_trades"]) + len(day_trades["option_day_trades"])
                        if num_day_trades + len(get_open_positions()) < 3:
                            # buy option
                            option_list.append(Option(stock, strike, opt_date, opt_type, buy=True))
                        else:
                            # record option but do not buy
                            option_list.append(Option(stock, strike, opt_date, opt_type, buy=False))

                elif 'SOLD' in item:
                    # sell options, but needs to check to see if they have been bought first
                    option_sold = item[1] + ' ' + item[2]

                    for opt in option_list:
                        if opt == option_sold:
                            opt.sell()

def main():
    live_options = get_active_options()

    while True:
        curr_time = str(datetime.now())[11:16]

        # pre-market, do nothing
        if curr_time < '07:30':
            time.sleep(20)

        # scrape server and trade during open hours
        elif curr_time >= '07:30' and curr_time < '14:00':
            day = str(date.today())
            scrape(day, live_options)
            get_prices(live_options)
            time.sleep(3)
        
        # post-market, do nothing
        elif curr_time >= '14:00':
            time.sleep(60)
        
        # something went wrong, print current time and kill program
        else:
            print('error')
            print(curr_time)
            cur.close()
            conn.close()
            break

if __name__ == "__main__":
    main()