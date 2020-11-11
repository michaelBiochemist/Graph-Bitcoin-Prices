#!/usr/bin/python3
import matplotlib.pyplot as plt
#import matplotlib.pylab as plt
import pandas as pd
import numpy as np
import math
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from datetime import datetime

import sys

register_matplotlib_converters()

# These are the hand-picked ranges for a line of best fit to be created against. 
# This is to prevent a linear regression line from being skewed by periods of enthusiasm or depression.
minima_ranges = {'bitcoin':(['2013-01-01','2014-01-01'],['2014-04-01','2015-04-01'],['2018-06-01','2019-04-01'])}

# Reads csv into object "a". Note: 'a' will denote a dataframe object throughout the rest of this file. 
# I was thinking of making it more readable, but 'a' is more concise, and substituting 'a' for "data_frame" would have to be done manually, which involves work.
def read_csv(file_name):
    a = pd.read_csv(file_name) 
    a['time_low'] = pd.to_datetime(a['time_low'],format='%Y-%m-%d')
    return a

# add calculated columns to dataframe. 
def prepare_dataframe(file_name):
	a = read_csv(file_name) 
	a['log_low'] = list(map(math.log10,a['low']))
	return a

# Checks if currency is included in minima_ranges. If so, then do linear regression on just that subsection of data. If not, do linear regression on the whole thing.
def get_line_of_best_fit(a, currency):
	minima = None
	if currency in minima_ranges.keys():
		for crange in minima_ranges[currency]:
		    c = a[(a['time_low'] > crange[0]) & (a['time_low'] < crange[1])]
		    min_open = min(c['open'])
		    d = c[c['open'] == min_open]
		    if minima is None:
		        minima = d
		    else:
		        minima = minima.append(d)
		minima['log_low'] = list(map(math.log10,minima['low']))
		ndates = mdates.date2num(minima['time_low'])
		z = np.polyfit(ndates,minima['log_low'],1)
		p0 = np.poly1d(z)
	else:
		z = np.polyfit(mdates.date2num(a['time_low']),a['log_low'],1)	
		p0 = np.poly1d(z)

#plt.plot(a['time_low'],p0(mdates.date2num(a['time_low'])),'xkcd:gold',a['time_low'],log_low)
a['best_fit'] = p0(mdates.date2num(a['time_low']))

if currency in minima_ranges.keys():
	q = a.plot(x='time_low',y=['log_low','best_fit'])
else:
	q = a.plot(x='time_low',y='log_low')
q.set_title('Logarithmic price vs Time')
q.set(xlabel='Date', ylabel='Log10 of price in $, so that 3=$1000 and 4=$10,000')


testy = mdates.date2num(datetime.strptime('2021-12-01','%Y-%M-%d'))
print(math.pow(10,p0(testy)))

plt.show()

if __name__ == '__main__':
	file_name = sys.argv[1]
	currency = file_name.split('_')[0]




"""
BELOW THIS IS OLD CODE, i'm mostly using it as reference for the graphing library, as i'm quite new to matplotlib.
exit()

#plt.plot(a['time_low'],p0(mdates.date2num(a['time_low'])),'xkcd:gold',a['time_low'],log_low)

fig, axs = plt.subplots(2)
fig.suptitle('Bitcoin Price Chart Logarithmic and Linear')
a['best_fit'] = p0(mdates.date2num(a['time_low']))
q = a.plot(x='time_low',y=['log_low','best_fit'])
plt.show()

# test this

axs[0].plot(a['time_low'],p0(mdates.date2num(a['time_low'])),'xkcd:gold',a['time_low'],log_low)
lval = p0(mdates.date2num(a['time_low']))
for i in range(0,len(lval)):
    lval[i] = math.pow(10,lval[i])

axs[1].plot(a['time_low'],lval,'xkcd:gold',a['time_low'],a['low'])
axs[0].set_title('Logarithmic Price')
axs[1].set_title('Linear Price')
axs[0].set(xlabel='time_low',ylabel='Log10 of Price')
axs[1].set(xlabel='time_low',ylabel='Bitcoin Price in Dollars')

fig.show()
"""
