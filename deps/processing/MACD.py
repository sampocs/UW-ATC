import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *
import talib, numpy

def macd (data):
	#Load config
	config = load_json("config.json")
	macdParams = config["MACD"]

	#Get MACD from talib
	data = numpy.array([float(x) for x in data])
	MACD = talib.MACD(data, macdParams["A"], macdParams["B"], macdParams["C"])

	#Get most recent value
	macLineArray = MACD[0]
	sigLineArray = MACD[1]
	macLine = macLineArray[len(macLineArray)-1]
	sigLine = sigLineArray[len(sigLineArray)-1]
	
	#Return to be added to processed data
	if (macLine > sigLine):
		state = "rising"
		distance = macLine - sigLine
	else:
		state = "falling"
		distance = sigLine - macLine
	mac = {
			"macdLine": macLine,
			"signalLine": sigLine,
			"state": state,
			"distance": distance
	}
	
	return mac

