from add_time import add_time
from datetime import date

class Option:
    prices_per_week=[]
    prices_per_day=[]

    daily_min_maxes={}
    all_time_min_max = (0.00,0.00)

    entry_price: float = 0.00
    def __init__(self, stock: str, strike: int, direction: str, option_date: str) -> None:
        self._stock = stock
        self._strike = strike
        self._direction = direction
        self._option_date = option_date
        self._date_bought = date.today()
        self._exp_date = self.add_exp_date() # how long program will watch option for default should be about a week or self._option_date

    def __str__(self) -> str:
        return f'{self._stock} {self._strike} {self._direction} {self._option_date}'

    def __repr__(self) -> str:
        return f'Option({self._stock}, {self._strike}, {self._direction}, {self._option_date})'

    def add_exp_date(self):
        exp = add_time(1, 'w')
        if exp > self._option_date:
            return self._option_date
        else:
            return exp

    def end_day(self):
        self.prices_per_week.append(self.prices_per_day)
    
    def is_same_as(self, other):
        if self._stock == other._stock and self._strike == other._strike and self._direction == other._direction and self._option_date == other._option_date:
            return True
        else:
            return False
