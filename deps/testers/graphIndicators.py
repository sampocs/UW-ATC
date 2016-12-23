import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *
import pandas as pd

proData = load_json("processedData.json")

#This file outputs data as a csv file
#The file can be opened in excel and easily graphed to confirm the values are accurate

#ICHIMOKU
baseLines = []
converLines = []
spanA = []
spanB = []
prices = []

j = 0
for i in proData["ichimoku"]:
	spanA.append(i["spanA"])
	spanB.append(i["spanB"])
	prices.append(proData["Price"][j])
	j = j + 1

df = pd.DataFrame({"prices": prices, "spanA": spanA, "spanB": spanB})
df.to_csv('graphIchimoku.csv', sep =',')

#MACD
macLine = []
sigLine = []

j = 0
for i in proData["MACD"]:
	macLine.append(i["macdLine"])
	sigLine.append(i["signalLine"])
	j = j + 1

df = pd.DataFrame({"macdLine": macLine, "signalLine": sigLine})
df.to_csv('graphMACD.csv', sep=',')

#RSI
rsi = []
top = []
bottom = []

j = 0
for i in proData["RSI"]:
	rsi.append(i)
	top.append(70)
	bottom.append(30)
	j = j + 1

df = pd.DataFrame({"rsi": rsi, "top": top, "bottom": bottom})
df.to_csv('graphRSI.csv', sep=',')

#ADX
adx = []
plusDI = []
minusDI = []

j = 0
for i in proData["ADX"]:
	adx.append(i["ADX"])
	plusDI.append(i["+DI"])
	minusDI.append(i["-DI"])
	j = j + 1

df = pd.DataFrame({"adx": adx, "plusDI": plusDI, "minusDI": minusDI})
df.to_csv('graphADX.csv', sep=',')

