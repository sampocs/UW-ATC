import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

def defineVariables():
	#Load info
	proData = load_json("processedData.json")

	#Grab import information
	ichimoku = proData["ichimoku"]
	length = len(ichimoku)

	#SpanA line
	currSpanA = ichimoku[length-1]["spanA"]
	pastSpanA = ichimoku[length-2]["spanA"]

	#SpanB line
	currSpanB = ichimoku[length-1]["spanB"]
	pastSpanB = ichimoku[length-2]["spanB"]

	#Cloud color
	currCloud = ichimoku[length-1]["cloudColor"]
	pastCloud = ichimoku[length-2]["cloudColor"]

	#Conversion line
	currConversion = ichimoku[length-1]["conversionLine"]
	pastConversion = ichimoku[length-2]["conversionLine"]

	##Price
	currPrice = proData["Price"][length-1]
	pastPrice = proData["Price"][length-2]

	return ichimoku, length, currSpanA, pastSpanA, currSpanB, pastSpanB, currCloud, pastCloud, currConversion, pastConversion, currPrice, pastPrice

#Price breaks through the cloud
def ichimokuCloudDecision ():
	ichimoku, length, currSpanA, pastSpanA, currSpanB, pastSpanB, currCloud, pastCloud, currConversion, pastConversion, currPrice, pastPrice = defineVariables()
	move = 0

	#If price just broke out of the cloud while rising
	#Buy, 1
	if (currCloud == "red"):
		if (pastPrice < pastSpanB and currPrice > currSpanB):
			move = 1
	#Sell, -1
	#If price just broke out of the cloud while falling
	elif (currCloud == "green"):
		if (pastPrice > pastSpanB and currPrice < currSpanB):
			move = -1
	#Hold
	else:
		move = 0

	return move

#Price crosses conversion line
def ichiConverDecision ():
	ichimoku, length, currSpanA, pastSpanA, currSpanB, pastSpanB, currCloud, pastCloud, currConversion, pastConversion, currPrice, pastPrice = defineVariables()
	move = 0

	#If price crossed conversion line while rising
	#Buy, 1
	if (pastPrice < pastConversion and currPrice > currConversion):
		move = 1

	#If price crossed conversion line while falling
	#Sell, -1
	elif (pastPrice > pastConversion and currPrice < currConversion):
		move = -1
	#Hold
	else:
		move = 0

	return move