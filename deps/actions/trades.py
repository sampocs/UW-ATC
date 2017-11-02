from jsonHandler import *
import oandapy

def executeTrade (dec):
	#Buy, sell, or hold
	decision = dec

	#Load Config
	config = load_json("config.json")

	#Load Processed Data
	proData = load_json("processedData.json")

	#Determine security of interest
	security = config["Security"]["CurrentSecurity"]

	confirmation = "Hold"
	#Stocks
	if (security == "Stocks"):
		confirmation = executeStockTrade(config, decision)
	#Currency
	elif (security == "Forex"):
		confirmation = executeForexTrade(config, decision)

	return confirmation

#Execute Stock trade and give confirmation message
def executeStockTrade(config, decision):
	#NO BROKER HAS BEEN CONNECTED YET TO FACILITATE THIS FUNCTION
	#Determine if there are open trades
	hasOpenTrades = False
	#Decision is buy, and there are no open positions
	if (decision == 1 and not hasOpenTrades):
		return "Bought"
	#Decision is sell, there are open positions, sell those positions
	elif (decision == -1 and hasOpenTrades):
		return "Sold"

	#Hold in all other situations
		#Decision is buy, but already have open positions
		#Decision is sell, but no open positions (can't short a stock)
		#Decision is hold
	else:
		return "Held"

#Execute Forex trade and give confirmation message
def executeForexTrade(config, decision):
	#If decison is to hold, no need to do anything
	if (decision != 0):

		#Create oanda client
		oandaDictionary = config["Security"]["Forex"]["oanda"]
		ACCESS_TOKEN = oandaDictionary["token"]
		ACCT_ID = oandaDictionary["id"]
		ENVIRONMENT = oandaDictionary["environment"]
		oanda = oandapy.API(environment=ENVIRONMENT, access_token=ACCESS_TOKEN)

		#Load data parameters
		dataParams = config["Security"]["Forex"]["dataParams"]
		stopLossPip = dataParams["stopLoss"]
		takeProfitPip = dataParams["takeProfit"]

		#Find units to trade if necessary
		numUnits = oandaDictionary["tradingUnits"]

		#Find if there is an open position
		positions = oanda.get_positions(ACCT_ID)
		hasOpenTrades = False;
		if (not(len(positions["positions"]) == 0)): #True if there is an open position
			for position in positions["positions"]:
				if (position["instrument"] == dataParams["instrument"]):
					hasOpenTrades = True;
					currPosition = position["side"]
					numUnits = int(position["units"]) #update number of units if necessary
		
		#If there is an open position, double the number of units to switch positions
		if (hasOpenTrades):
			numUnits = 2 * numUnits
		units = str(numUnits)

		#Find dictionary of bid and ask prices
		response = oanda.get_prices(instruments=dataParams["instrument"])
		price = response["prices"][0]


		#If decision is to buy, and there are no open positions
		#Or if decision is to buy, and there is an open position that was short
		#Buy
		if ((decision == 1 and not hasOpenTrades) \
				or (decision == 1 and hasOpenTrades and currPosition == "sell")):
			#Find bid price
			price = price["bid"]
			#Stop Loss
			stopLoss = price - stopLossPip
			#Take Profit
			takeProfit = price + takeProfitPip
			#Make Trade
			oanda.create_order(ACCT_ID, instrument=dataParams["instrument"], units=units, side="buy", type="market", stopLoss=stopLoss, takeProfit=takeProfit)
			
			#Return Confirmation Message
			return "Bought {} units of {} at {}".format(units, dataParams["instrument"], price)


		#If decision is to sell, and there are no open positions
		#Or if decision is to sell, and there is an open position that was a buy
		#Sell
		elif (decision == -1 and not hasOpenTrades \
			or (decision == -1 and hasOpenTrades and currPosition == "buy")):
			#Find ask price
			price = price["ask"]
			#Stop Loss
			stopLoss = price + stopLossPip
			#Take Profit
			takeProfit = price - takeProfitPip
			#Make Trade
			oanda.create_order(ACCT_ID, instrument=dataParams["instrument"], units=units, side="sell", type="market", stopLoss=stopLoss, takeProfit=takeProfit)

			#Return Confirmation Message
			return "Sold {} units of {} at {}".format(units, dataParams["instrument"], price)


		#Otherwise hold
		else:
			return "Held"









