import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

from getData import getForexPrices, getForexBidAsk
from processData import processD
from processPolicies import processP

#Load parameters
config = load_json("config.json")
dataParams = config["Security"]["Forex"]["dataParams"]
stopLoss = dataParams["stopLoss"]
takeProfit = dataParams["takeProfit"]
units = config["Security"]["Forex"]["oanda"]["tradingUnits"]

#Information to store
numTradesMade, boughtAt, soldAt = 0,0,0
profit = []
hasOpenTrades = False
position = None

#Get data
data = getForexPrices(dataParams["granularity"])
closeBid, closeAsk = getForexBidAsk()

#Start at the 80th datapoint and run til the end
begin = 0
closedEarly = False
for current in range(80, len(data)):
	#Grab relevant data
	relData = data[begin:current]
	begin = begin + 1
	bidPrice = closeBid[current]
	askPrice = closeAsk[current]

	#Process data
	processD(relData)

	#Process policies
	decision = processP()

	#No open positions
	if (not hasOpenTrades):
		#Hold
		if (decision == 0):
			continue
		#Buy
		elif (decision == 1):
			boughtAt = askPrice
			position = "long"
			numTradesMade = numTradesMade + 1
			hasOpenTrades = True
			continue
		#Sell
		else:
			soldAt = bidPrice
			position = "short"
			numTradesMade = numTradesMade + 1
			hasOpenTrades = True
			continue

	#There are open positions
	else:
		#Check current position
		#Open long
		if (position == "long"):
			#Take profit and stop loss
			if ((bidPrice >= boughtAt + takeProfit) or (bidPrice <= boughtAt - stopLoss)):
				#Calculate Profit
				newProfit = (units * (bidPrice - boughtAt)) / bidPrice
				profit.append(newProfit)
				#Update Status
				hasOpenTrades = False
				position = None
				continue
			#Decsion is to buy or hold
			#Hold
			elif (decision == 1 or decision == 0):
				continue
			#Decision is to sell, switch positions and short
			else:
				#Close current trade - calculate profit
				newProfit = (units * (bidPrice - boughtAt)) / bidPrice
				profit.append(newProfit)
				#Switch positions - update status
				soldAt = bidPrice
				position = "short"
				numTradesMade = numTradesMade + 1
				continue

		#Open short
		elif (position == "short"):
			#Take profit and stop loss
			if ((askPrice <= soldAt - takeProfit) or (askPrice >= soldAt + stopLoss)):
				#Calculate Profit
				newProfit = (units * (askPrice - soldAt)) / askPrice
				profit.append(newProfit)
				#Update Status
				hasOpenTrades = False
				position = None
				continue
			#Decision is to sell or hold
			#Hold
			elif (decision == -1 or decision == 0):
				continue
			#Decison is to buy, switch positons and long
			else:
				#Close Current trade - calculate profit
				newProfit = (units * (askPrice - soldAt)) / askPrice
				profit.append(newProfit)
				#Switch positions - update status
				boughtAt = bidPrice
				position = "long"
				numTradesMade = numTradesMade + 1
				continue

		#Final value, close everything out
		if (current == len(data) - 1):
			if (hasOpenTrades):
				closedEarly =True
				if (position =="long"):
					newProfit = (units * (bidPrice - boughtAt)) / bidPrice
					profit.append(newProfit)
				elif (position == "short"):
					newProfit = (units * (askPrice - soldAt)) / askPrice
					profit.append(newProfit)

#COMPLILE RESULTS
#List of policies used
policies = []
policyList = ""
for indicator in config["Policies"]:
	if (config["Policies"][indicator]):
		policies.append(indicator)
for i in range(0,len(policies)):
	if (i == len(policies)-1):
		policyList = policyList + policies[i]
	else:
		policyList = policyList + policies[i] + ", "

#Compile return message 
totalProfit = sum(profit)
percentReturn = 100 * float(totalProfit / units)
resultsMessage = "{} trades were executed.\nTotal Profit = ${}\n{} units were traded at a time.\nTotal Return = {}%". \
					format(numTradesMade, totalProfit, units, percentReturn)

#Print results
print "Indicators used were: " + policyList
print resultsMessage
print "Profit from each trade was as follows:"
print profit
if (closedEarly):
	print "Last position was closed prematurely."
