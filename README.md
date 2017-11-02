# UW-ATC
Pipeline for using technical analysis to make automated trades in the stock or foreign exchange market.
##Usage
In the Config File:
  * Change the "CurrentSecurity" to either Stocks or Forex.
  * Enter in the desired data parameters (Instrument/Ticker, Period/Granularity, Stop Loss/Take Profit)
    * In Forex, granularity represents the time interval of successive data points
      * Ex: M10 means every 10 minutes, H4 means every 4 hours, etc.
    * With Stocks, period is the time interval in seconds.
  * Under "Policies", change the preferred indicators to "true".
  * Under "Actions", change the desired actions for to "true". The action will only occur when a possible successful position ahs been identified.
    * If you want to recieve a text, insert your Twilio account information under "Twilio".
    * If you want to recieve an email, enter your email address and password under "Email".
    * If you want to automatically execute a trade in the foreign exchange market, enter your Oanda account information and the number of units you would like to trade.

## Dependencies
* OandaPy
* TA-Lib
* Twilio
* Numpy
* Requests 
* rfc3339 
