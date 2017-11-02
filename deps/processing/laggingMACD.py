import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *
import talib, numpy

from getData import getStockPrices, getForexPrices

def macd2 ():
	#Load Config
	config = load_json("config.json")
	macdParams = config["MACD"]

	#Determine security type and number of data values that need to be analyzed
	security = config["Security"]["CurrentSecurity"]
	daysBack = config["Security"][security]["dataParams"]["daysBack"]

	data = []
	#Stocks
	if (security == "Stocks"):
		period = macdParams["LaggingStock"]
		data = getStockPrices (period)
	#Currencies
	elif (security == "Forex"):
		granularity = macdParams["LaggingForex"]
		data = getForexPrices(granularity)

	#Use talib to find the lagging MACD values
	data = numpy.array([float(x) for x in data])
	MACD = talib.MACD(data, macdParams["A"], macdParams["B"], macdParams["C"])
	macLineArray = MACD[0]
	sigLineArray = MACD[1]

	#Create array of dictionaries to add to processed data
	macd = []
	for i in range (len(data) - daysBack, len(data)):
		macLine = macLineArray[i]
		sigLine = sigLineArray[i]
		if (macLine > sigLine):
			state = "rising"
			distance = macLine - sigLine
		else:
			state = "falling"
			distance = sigLine - macLine
		mac = {
				"macdLine": macLine,
				"signalLine": sigLine,
				"state": state,
				"distance": distance
		}
		macd.append(mac)
	return macd

