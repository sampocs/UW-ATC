import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

#Buys or sells when the plus and minus directional indicators cross
#And the adx indicates a strong trend is present
def adxDecision ():
	#Load information
	config = load_json("config.json")
	proData = load_json("processedData.json")
	adx = proData["ADX"]

	#Grab import information
	currADX = adx[-1]["ADX"]
	currPlusDI = adx[-1]["+DI"]
	pastPlusDI = adx[-2]["-DI"]
	currMinusDI = adx[-1]["+DI"]
	pastMinusDI = adx[-2]["-DI"]

	#If ADX is above the given threshold, the trend is considered strong
	if (currADX > config["ADX"]["strongTrend"]):
		#If the plus directional indicator crosses above the minus directional indicator
		#Buy, 1
		if (pastPlusDI < pastMinusDI and currPlusDI > currMinusDI):
			move = 1
		#If the minus directional indicator crosses above the plus directional indicator
		#Sell, -1
		elif (pastMinusDI < pastPlusDI and currMinusDI > currPlusDI):
			move = -1
		#Hold, 0
		else:
			move = 0
	#Trend isn't considered strong, hold
	else:
		move = 0

	return move
	