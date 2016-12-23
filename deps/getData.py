import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from jsonHandler import *
import requests, csv, re, json

import time
import datetime as dt
from rfc3339 import rfc3339

#load config
config = load_json("config.json")

#Determine security to use
security = config["Security"]["CurrentSecurity"]

#get data
def getPrices():
	#Stocks
	if (security == "Stocks"):
		period = config["Security"]["Stocks"]["dataParams"]["period"]
		return getStockPrices (period)
	#Currencies
	elif (security == "Forex"):
		granularity = config["Security"]["Forex"]["dataParams"]["granularity"]
		return getForexPrices(granularity)

#Stocks
def getStockPrices (granularity):
	#Load parameters
	dataPararms = config["Security"]["Stocks"]["dataParams"]
	ticker = dataPararms["ticker"]
	period = granularity
	days = dataPararms["days"]

	#Get data from google finance API
	url = 'http://www.google.com/finance/getprices?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'\
	.format(ticker=ticker, period=period, days=days)

	prices = requests.get(url)
	reader = csv.reader(prices.text.splitlines())
	times = []
	data = []
	lastStamp = 0

	#Grab prices and times from csv
	for line in reader:
		if re.match('^[a\d]', line[0]):
			#Each line that starts with 'a' gives the full time
			if line[0].startswith("a"):
				#Time
				time = int(line[0][1:])
				lastStamp = time
				times.append(str(dt.datetime.fromtimestamp(time)))
				#Close price (line[1])
				data.append(float(line[1])) 
			#Lines after the line with 'a', give the seconds elapse since last 'a' line
			else:
				#Time
				time = lastStamp+(int(line[0]) * 60)
				times.append(str(dt.datetime.fromtimestamp(time)))
				#Close price (line[1])
				data.append(float(line[1])) 

	return data

#Currencies
def getForexPrices(granularity):
	#Load parameters
	dataParams = config["Security"]["Forex"]["dataParams"]
	inst = dataParams["instrument"]
	gran = granularity
	count = dataParams["count"]
	candleFormat = dataParams["candleFormat"]
	endtime = getCurrentTime()

	#Get dictionary of candles
	candles = getForexCandles(inst, gran, count, endtime, candleFormat)

	#Store prices and times
	data = []
	time = []
	for i in candles:
		data.append(i.get("closeMid"))
		time.append(i.get("time"))

	return data


#Time Formatting
def getCurrentTime ():
	#Get Unix Time
	timestamp = int(time.time())
	#Fix TimeZone Issue
	timestamp = timestamp + 21600 -3000000
	#Change format
	t = dt.datetime.fromtimestamp(timestamp)
	t = rfc3339(t)
	t = str(t)
	t = t[:-6]

	#Evaluate
	day = t[0:10]
	hour = t[11:13]
	minute = t[14:16]
	sec = t[17:19]

	#Format for oanda
	currTime = day + "T" + hour + "%3A" + minute + "%3A" + sec

	return currTime


#HIGH/LOW PRICES
#Stocks
def getStocksHighLow ():
	#Load parameters
	dataParams = config["Security"]["Stocks"]["dataParams"]
	ticker = dataParams["ticker"]
	period = dataParams["period"]
	days = dataParams["days"]

	#Get prices from google finance API
	url = 'http://www.google.com/finance/getprices?i={period}&p={days}d&f=d,o,h,l,c,v&df=cpct&q={ticker}'\
	.format(ticker=ticker, period=period, days=days)

	prices = requests.get(url)
	reader = csv.reader(prices.text.splitlines())

	#Grab high, low, and close prices
	highAsk, lowAsk, closeAsk = [], [], []
	for line in reader:
		#First line with prices starts with 'a'
		if re.match('^[a\d]', line[0]):
			#Close, high, and low (line[1], line[2], line[3])
			closeAsk.append(float(line[1]))
			highAsk.append(float(line[2]))
			lowAsk.append(float(line[3]))
	return highAsk, lowAsk, closeAsk

#Forex
def getForexHighLow ():
	#Load parameters
	dataParams = config["Security"]["Forex"]["dataParams"]
	endtime = getCurrentTime ()

	#Get dictionary of midpoint candles
	candles = getForexCandles(dataParams["instrument"], dataParams["granularity"], dataParams["count"], endtime, "midpoint")

	#Grab high, low, and close prices
	highMid, lowMid, closeMid = [], [], []
	for i in candles:
		highMid.append(i.get("highMid"))
		lowMid.append(i.get("lowMid"))
		closeMid.append(i.get("closeMid"))

	return highMid, lowMid, closeMid

#BID/ASK PRICES
def getForexBidAsk ():
	#Load parameters
	dataParams = config["Security"]["Forex"]["dataParams"]
	endtime = getCurrentTime ()

	#Get dicitonary  of bid and ask prices
	candles = getForexCandles(dataParams["instrument"], dataParams["granularity"], dataParams["count"], endtime, "bidask")

	#Grab the close bid and ask prices
	closeBid, closeAsk = [], []
	for i in candles:
		closeBid.append(i.get("closeBid"))
		closeAsk.append(i.get("closeAsk"))

	return closeBid, closeAsk

#Calls oanda API
def getForexCandles (instrument, granularity, count, endtime, candleFormat):
	#Format URL
	url = 'https://api-fxpractice.oanda.com/v1/candles?instrument={instrument}&granularity={granularity}&count={count}&end={time}&candleFormat={candleFormat}'\
	.format(instrument=instrument, granularity=granularity, count=count, time=endtime, candleFormat=candleFormat)

	r = requests.get(url)
	candles = r.json().get('candles')

	return candles
