import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/policies")
from jsonHandler import *

from MACDpolicy import macdDecision
from DualMACD import dualMACdecision
from RSIpolicy import rsiDecision
from IchimokuPolicy import ichimokuCloudDecision, ichiConverDecision
from ADXpolicy import adxDecision

#Reads processed data and comes up with a final decision
def processP ():
	#Load Config
	config = load_json("config.json")
	togglePolicy = config["Policies"] #List of policies to take into consideration
	threshold = config["DecisionThreshold"] #Threshold for confident decision

	#BUILD POLICYRESULTS
	policyResults = {}

	#MACD
	policyResults["MACD"] = macdDecision()

	#Dual MACD
	policyResults["DualMACD"] = dualMACdecision()

	#RSI 
	policyResults["RSI"] = rsiDecision()

	#Ichimoku
	policyResults["IchimokuCloud"] = ichimokuCloudDecision() #Cloud
	policyResults["IchimokuConversionLine"] = ichiConverDecision() #ConversionLine

	#ADX
	policyResults["ADX"] = adxDecision ()


	#COME UP WITH FINAL DECISION
	numOfPolicies, combinedDecisions = 0, 0

	#Find policies to consider and find the average decision
	for policy in policyResults:
		if togglePolicy[policy]: #True if the policy should be taken into consideration 
			numOfPolicies = numOfPolicies + 1
			combinedDecisions = combinedDecisions + policyResults[policy]
	finalDecision = float(combinedDecisions / numOfPolicies)

	#Add decision to policyResults
	policyResults["finalDecision"] = finalDecision

	#Create PolicyResults JSON
	write_json("policyResults.json", policyResults)


	#TAKE CONFIDENCE THRESHOLD INTO CONSIDERATION AND ROUND
	#If confidence is above threshold to buy
	if (finalDecision > threshold["Buy"]):
		finalDecision = 1
	#If confidence is below threshold to sell
	elif (finalDecision < threshold["Sell"]):
		finalDecision = -1
	#Hold
	else: 
		finalDecision = 0

	return finalDecision
	


