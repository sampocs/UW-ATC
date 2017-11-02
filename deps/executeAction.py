import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/actions")
from jsonHandler import *
import alerts, trades

def action (dec):
	#Buy, sell, or hold
	decision = dec

	#Load Config
	config = load_json("config.json")
	actions = config["Actions"]

	tradeConfirmation = None #Changed only if a trade was executed
	#Execute a trade if requested
	if (actions["ExecuteTrade"]):
		tradeConfirmation = trades.executeTrade(decision) #Returns confirmation message

	#Find actions to be taken into consideration
	if (tradeConfirmation != "Held"):
		for action in actions:
			if actions[action]: #True if they should be taken into consideration
				#Alerts
				if (action != "ExecuteTrade"):	
					function = getattr(alerts, action)
					function(decision, tradeConfirmation)
					