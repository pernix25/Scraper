from datetime import date, datetime
import sqlite3 as db
import robin_stocks.robinhood as rh

class Option:
    def __init__(self, ticker : str, strike : str, exp_date : str, opt_type : str, opt_desc = None, opt_id = None, new_opt = True, buy = False) -> None:
        self.ticker = ticker
        self.strike = strike
        self.exp_date = exp_date
        self.opt_type = opt_type
        self.opt_desc = opt_desc
        self.option_id = opt_id
        self.qnty = self.get_quantity()
        self.bought = buy
        self.date_bought = str(date.today())

        if buy:
            self.buy()

        if new_opt:
            data = rh.get_option_market_data(self.ticker, self.exp_date, self.strike, self.opt_type)[0][0]

            self.open_interest = data['open_interest']
            self.volume = data['volume']
            self.cpl = data['chance_of_profit_long']
            self.cps = data['chance_of_profit_short']
            self.delta = data['delta']
            self.gamma = data['gamma']
            self.rho = data['rho']
            self.theta = data['theta']
            self.vega = data['vega']
            self.iv = data['implied_volatility']

            self.upload_new_opt()

    def upload_new_opt(self) -> None:
        # uploads option data to database
        conn = db.connect('Scraper.db')
        cur = conn.cursor()

        # checks to see if option is a lotto or if its not bought then gets current price
        if self.opt_desc or not self.bought:
            self.bp = self.get_curr_price()

        # gets ticker_id from db or inserts new ticker_desc
        cur.execute(f"SELECT ticker_desc FROM Stocks;")
        stocks = cur.fetchall()
        if stocks:
            stocks = [stock[0] for stock in stocks]
        if self.ticker not in stocks:
            cur.execute(f"INSERT INTO Stocks (ticker_desc) VALUES (?)", (self.ticker,))
            conn.commit()
            cur.execute("SELECT ticker_id FROM Stocks WHERE ticker_desc = ?", (self.ticker,))
        else:
            cur.execute("SELECT ticker_id FROM Stocks WHERE ticker_desc = ?", (self.ticker,))
        ticker_id = cur.fetchone()[0]

        # sets type_id for db based on opt_type
        if self.opt_type == 'call':
            type_id = 1
        else:
            type_id = 2

        # inserts option info into Options table
        cur.execute(f"INSERT INTO Options (ticker_id, strike, exp_date, strategy_id, type_id, opt_desc, qnty, bp, open_interest, volume, iv, cpl, cps, gamma, delta, theta, rho, vega) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (ticker_id, self.strike, self.exp_date, 2, type_id, self.opt_desc, self.qnty, self.bp, self.open_interest, self.volume, self.iv, self.cpl, self.cps, self.gamma, self.delta, self.theta, self.rho, self.vega))
        conn.commit()

        # gets option_id from db; assigns to self
        cur.execute(f"SELECT option_id FROM Options WHERE ticker_id = ? AND strike = ? AND exp_date = ?", (ticker_id, self.strike, self.exp_date))
        self.option_id = cur.fetchone()[0]

        # Inserts bought price and inserts option into ActiveOptions
        cur.execute(f"INSERT INTO Prices (option_id, price, tmstp) VALUES (?,?,?)", (self.option_id, self.bp, str(datetime.now())[:18]))
        conn.commit()
        cur.execute(f"INSERT INTO ActiveOptions (option_id) VALUES (?)", (self.option_id,))
        conn.commit()

        cur.close()
        conn.close()

    def buy(self) -> None:
        # buys option on robinhood
        opt_price = rh.get_option_market_data(self.ticker, self.exp_date, self.strike, self.opt_type)[0][0]["ask_price"]
        rh.order_buy_option_limit(positionEffect="open", creditOrDebit="debit", price=opt_price, symbol=self.ticker, quantity=self.qnty, expirationDate=self.exp_date, strike=self.strike, optionType=self.opt_type, timeInForce="gfd")
        self.bp = opt_price

    def sell(self) -> None:
        # sells option on robinhood if there are less than or equal to 3 day trades
        day_trades = rh.account.get_day_trades()
        if len(day_trades["equity_day_trades"]) + len(day_trades["option_day_trades"]) >= 3:
            print("day trade protection; cannot sell")
            return None
        else:
            opt_price = rh.get_option_market_data(self.ticker, self.exp_date, self.strike, self.opt_type)[0][0]["ask_price"]
            rh.order_sell_option_limit(positionEffect="close", creditOrDebit="credit", price=opt_price, symbol=self.ticker, quantity=self.qnty, expirationDate=self.exp_date, strike=self.strike, optionType=self.opt_type, timeInForce="gfd")

    def get_curr_price(self) -> str:
        # gets current price of option
        return rh.get_option_market_data(self.ticker, self.exp_date, self.strike, self.opt_type)[0][0]["ask_price"]

    def get_quantity(self, price=0) -> int:
        # gets max quantity of option based on a particular price
        if price == 0:
            return 1
        else:
            opt_price = rh.get_option_market_data(self.ticker, self.exp_date, self.strike, self.opt_type)[0][0]["ask_price"]
            return (price // (opt_price * 100))

    def __repr__(self) -> str:
        return f"Option({self.ticker}, {self.strike}, {self.exp_date}, {self.opt_type}, {self.qnty}, {self.opt_desc})"

    def __str__(self) -> str:
        if self.opt_type == 'call': 
            opt = 'C' 
        else: 
            opt = 'P'
        return f"{self.ticker} {self.strike}{opt}"

    def __eq__(self, other: str) -> bool:
        if str(self) == other:
            return True
        else:
            return False
