import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *

def ichimokuProcess (data):
	#Load config and parameters
	config = load_json("config.json")
	ichiParams = config["ichimoku"]
	a = ichiParams["A"]
	b = ichiParams["B"]
	c = ichiParams["C"]

	#PRESENT CONVERSION AND BASE, FUTURE CLOUD
	dayA = [data[i] for i in range (len(data) - a, len(data))]
	dayB = [data[i] for i in range (len(data) - b, len(data))]
	dayC = [data[i] for i in range (len(data) - c, len(data))]

	#A days high and low
	highA = max(dayA)
	lowA = min(dayA)
	#B days high and low
	highB = max(dayB)
	lowB = min(dayB)
	#C days high and low
	highC = max(dayC)
	lowC = min(dayC)

	#conversion line present
	conver = (highA + lowA)/2.0
	#base line present
	base = (highB + lowB)/2.0
	#cloud lines B days in the future
	spanAFut = (conver + base)/2.0
	spanBFut = (highC + lowC)/2.0

	#PAST CONVERSION AND BASE, PRESENT CLOUD
	dayAPast = [data[i] for i in range (len(data) - a-b, len(data) - b)]
	dayBPast = [data[i] for i in range (len(data) - b-b, len(data) - b)]
	dayCPast = [data[i] for i in range (len(data) - c-b, len(data) - b)]

	#A days high and low
	highAPast = max(dayAPast)
	lowAPast = min(dayAPast)
	#B days high and low
	highBPast = max(dayBPast)
	lowBPast = min(dayBPast)
	#C days high and low
	highCPast = max(dayCPast)
	lowCPast = min(dayCPast)

	#conversion line past
	converPast = (highAPast + lowAPast)/2.0
	#base line past
	basePast = (highBPast + lowBPast)/2.0
	#cloud lines present
	spanA = (converPast + basePast)/2.0
	spanB = (highCPast + lowCPast)/2.0

	if (spanA > spanB):
		color = "green"
	else:
		color = "red"

	ichi = {
				"conversionLine": conver,
				"baseLine": base,
				"spanA": spanA,
				"spanB": spanB,
				"cloudColor": color
			}

	return ichi



