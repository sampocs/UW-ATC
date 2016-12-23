import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

#Buys or sells when the MACD line and signal line cross
def macdDecision ():
	#Load info
	proData = load_json("processedData.json")

	#Gather information
	macd = proData["MACD"]
	currentState = macd[len(macd)- 1]["state"]
	pastState = macd[len(macd) - 2]["state"]
	move = 0

	#Was falling, now it's rising, buy, 1
	if (pastState == "falling" and currentState == "rising"):
		move = 1
	#Was rising, now it's falling, sell, -1
	elif (pastState == "rising" and currentState == "falling"):
		move = -1
	#hold
	else:
		move = 0

	return move