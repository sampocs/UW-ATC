import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
from jsonHandler import *
import pandas as pd

proData = load_json("processedData.json")

#This file outputs data as a csv file
#The file can be opened in excel and easily graphed to confirm the values are accurate

#ICHIMOKU
baseLines, converLines, spanA, spanB, prices = [], [], [], [], []

for j, i in enumerate(proData["ichimoku"]):
	spanA.append(i["spanA"])
	spanB.append(i["spanB"])
	prices.append(proData["Price"][j])

df = pd.DataFrame({"prices": prices, "spanA": spanA, "spanB": spanB})
df.to_csv('graphIchimoku.csv', sep =',')

#MACD
macLine, sigLine = [], []

for j, i in enumerate(proData["MACD"]):
	macLine.append(i["macdLine"])
	sigLine.append(i["signalLine"])

df = pd.DataFrame({"macdLine": macLine, "signalLine": sigLine})
df.to_csv('graphMACD.csv', sep=',')

#RSI
rsi, top, bottom = [], [], []

for j, i in enumerate(proData["RSI"]):
	rsi.append(i)
	top.append(70)
	bottom.append(30)

df = pd.DataFrame({"rsi": rsi, "top": top, "bottom": bottom})
df.to_csv('graphRSI.csv', sep=',')

#ADX
adx, plusDI, minusDI = [], [], []

for j, i in enumerate(proData["ADX"]):
	adx.append(i["ADX"])
	plusDI.append(i["+DI"])
	minusDI.append(i["-DI"])

df = pd.DataFrame({"adx": adx, "plusDI": plusDI, "minusDI": minusDI})
df.to_csv('graphADX.csv', sep=',')

