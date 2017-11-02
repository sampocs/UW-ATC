import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/deps")

from getData import getPrices
from processData import processD
from processPolicies import processP
from executeAction import action

#Get data
data = getPrices()

#Process data 
processD(data)

#Apply policies
decision = processP()

#Actions
action(decision)

