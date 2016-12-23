import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *
from getData import getStocksHighLow, getForexHighLow
import talib, numpy, requests, json

def adxProcess (): 
	#Load config
	config = load_json("config.json")
	adxParams = config["ADX"]
	security = config["Security"]["CurrentSecurity"]
	daysBack = config["Security"][security]["dataParams"]["daysBack"]

	#Get high, low, and close prices from getData.py
	#Stocks
	if (security == "Stocks"):
		highAsk, lowAsk, closeAsk = getStocksHighLow ()
	#Forex
	else:
		highAsk, lowAsk, closeAsk = getForexHighLow ()

	#Format for talib
	highAsk = [float(x) for x in highAsk]
	lowAsk = [float(x) for x in lowAsk]
	closeAsk = [float(x) for x in closeAsk]
	highAsk = numpy.array(highAsk)
	lowAsk = numpy.array(lowAsk)
	closeAsk = numpy.array(closeAsk)
	
	#Get ADX from talib
	ADX = talib.ADX(highAsk, lowAsk, closeAsk, adxParams["A"])
	plusDirection = talib.PLUS_DI(highAsk, lowAsk, closeAsk, adxParams["A"])
	minusDirection = talib.MINUS_DI(highAsk, lowAsk, closeAsk, adxParams["A"])

	#Create array of dictionaries to add to processed data
	adx = []
	for i in range (len(highAsk) - daysBack, len(highAsk)):
		adxPart = {
				'ADX': ADX[i],
				'+DI': plusDirection[i],
				'-DI': minusDirection[i]
		}
		adx.append(adxPart)

	return adx

