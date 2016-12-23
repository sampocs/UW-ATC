import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

#Returns to buy or sell if the long term and short term MACD are in the same state
def dualMACdecision ():
	#Load info
	proData = load_json("processedData.json")

	#Gather information
	#Short term
	macd = proData["MACD"] 
	currentState = macd[len(macd)- 1]["state"]
	pastState = macd[len(macd) - 2]["state"]
	#Long term
	laggingMACD = proData["LaggingMACD"]
	laggingState = laggingMACD[len(laggingMACD) - 1]["state"]
	move = 0

	#If was falling, now rising; buy, 1
	if (pastState == "falling" and currentState == "rising"):
		if (laggingState == "rising"): #long term
			move = 1
	#If was rising, now falling; sell, -1
	elif (pastState == "rising" and currentState == "falling"):
		if (laggingState == "falling"): #long term
			move = -1
	#hold
	else:
		move = 0

	return move