import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *
import talib, numpy

def rsiProcess (data):
	#Load config and rsi parameters
	config = load_json("config.json")
	span = config["RSI"]["span"]

	#Get rsi with talib
	data = [float(x) for x in data]
	data = numpy.array(data)
	rsi = talib.RSI(data, timeperiod=span)
	rsiVal = rsi[len(rsi)-1]
	
	return rsiVal




