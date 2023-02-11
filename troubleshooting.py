from option_class import *


x = Option('TSLA', '175', 'call', '2023-01-20')
y = Option('AMZN', '100', 'put', '2023-03-25')
x.entry_price = 0.69
x.prices_per_week = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]

print(x._option_date)
print(x._date_bought)
print(x._exp_date)
#print()