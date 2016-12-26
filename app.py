import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/deps")

from getData import getPrices
from processData import processD
from processPolicies import processP
from executeAction import action

#get data
data = getPrices()

#process data
processD(data)

#policies
decision = processP()

#actions
action(1)

