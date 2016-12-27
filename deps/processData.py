import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/processing")
from jsonHandler import *

from MACD import macd
from laggingMACD import macd2
from ichimoku import ichimokuProcess
from RSI import rsiProcess
from ADX import adxProcess

#load config
config = load_json("config.json")
security = config["Security"]["CurrentSecurity"]
daysBack = config["Security"][security]["dataParams"]["daysBack"]

def processD (data):		
	#sections of processed data
	proData = {}
	proData["Price"] = []
	proData["MACD"] = []
	proData["LaggingMACD"] = []
	proData["RSI"] = []
	proData["ichimoku"] = []
	proData["ADX"] = []

	#iterate through necessary data
	index = 0
	laggingRan = False
	adxRan = False

	for i in range (len(data)-daysBack, len(data)):

		#relevant data
		relData = data[:len(data)-(daysBack-index-1)]

		#price
		proData["Price"].append(data[i])
				
		#MACD
		mac = macd(relData)
		proData["MACD"].append(mac)

		#Lagging MACD
		if (not laggingRan):
			mac2 = macd2()
			proData["LaggingMACD"] = mac2
			laggingRan = True

		#ichimoku
		ichi = ichimokuProcess(relData)
		proData["ichimoku"].append(ichi)

		#RSI
		rsi = rsiProcess(relData)
		proData["RSI"].append(rsi)

		#ADX
		if (not adxRan):
			adx = adxProcess()
			proData["ADX"] = adx
			adxRan = True

		#update index
		index = index + 1

	#Output dictionary as processed data file
	write_json("processedData.json", proData)
