from jsonHandler import *
from twilio.rest import TwilioRestClient
import smtplib

def SendText (decision, confirmation):
	#If decision is to hold, don't do anything
	if (decision != 0):
		#If no trade has been executed, create a new message
		if (confirmation == None):
			message = decisionMessage(decision)
		#If a trade has been executed, send the confirmation
		else: 
			message = confirmation
		
		#Send a text using twilio
		config = load_json("config.json")
		twilio = config["Twilio"]
		client = TwilioRestClient(twilio["sid"], twilio["token"])
		client.messages.create(to = twilio["to"], from_ = twilio["from"], body = message)
	
def SendEmail (decision, confirmation):
	#If decision is to hold, don't do anything
	if (decision != 0):
		#If no trade has been executed, create a new message
		if (confirmation == None):
			message = decisionMessage(decision)
		#If a trade has been executed, send the confirmation
		else: 
			message = confirmation
	
		#Send an email
		config = load_json("config.json")
		email = config["Email"]
		server = smtplib.SMTP('smtp.gmail.com', 587) 
		server.starttls()
		server.login(email["from"], email["password"])
		server.sendmail(email["from"], email["to"], message)
		server.quit()

def decisionMessage (decision):
	#Load necessary information
	config = load_json("config.json")
	proData = load_json("processedData.json")
	securityType = config["Security"]["CurrentSecurity"]

	#Find the current price
	priceArray = proData["Price"]
	price = priceArray[-1]

	#Stocks
	if (securityType == "Stocks"):
		ticker = config["Security"][securityType]["dataParams"]["ticker"]
		#Buy	
		if (decision == 1):
			return "Buy {}. Current price is: ${} per share.".format(ticker, price)
		#Sell
		elif (decision == -1):
			return "Sell shares of {}. Current price is ${} per share.".format(ticker, price)

	#Forex
	else:
		instrument = config["Security"][securityType]["dataParams"]["instrument"]
		#Buy
		if (decision == 1):
			return "Buy {}. Current price is {}.".format(instrument, price)
		#Sell
		elif (decision == -1):
			return "Short {}. Current price is {}.".format(instrument, price)
			
	return ""



