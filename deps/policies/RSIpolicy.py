import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

#Buys or sells if the RSI is oversold or overbought
def rsiDecision ():
	#Load info
	config = load_json("config.json")
	proData = load_json("processedData.json")
	
	#Gather information
	rsi = proData["RSI"]
	currentRSI = rsi[-1]
	pastRSI = rsi[-2]
	upper = config["RSI"]["upper"]
	lower = config["RSI"]["lower"]
	move = 0

	#oversold, buy, 1
	if (pastRSI > lower and currentRSI < lower):
		move = 1
	#overbought, sold, -1
	elif (pastRSI < upper and currentRSI > upper):
		move = -1
	#hold
	else: 
		move = 0

	return move

