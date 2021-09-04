# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 16:34:36 2021

Demonstration for how to use chanceCalc in Monte Carlo simulation.

@author: PM.org
"""
import pandas as pd
import json
import chanceCalc as cC
from numpy import mean

#Setting up our variables, price per unit, cost per unit, the average demand, 
#and the number of units we chose to produce
cost_per_unit = 30
price_per_unit = 40
production_decision = 100000
demand = 100000

#Calculating cost/revenue/profit
cost = cost_per_unit * production_decision
print("Cost: "+str(cost))
revenue = price_per_unit * demand
print("Reveue: "+str(revenue))
profit = revenue - cost
print("Profit: "+str(profit))

#To add uncertainty from chanceCalc, we pull in the SIPmath files carrying our 
#SIP
file_name = 'Demand_Forecast_Library.SIPmath'
data = open(file_name,)
jsonform = json.load(data)
dumps = json.dumps(jsonform)
SIPs = cC.ImportJSON(dumps)

#Now we have our sip and we can simulate 1000 trials
demand_sip = SIPs.simulateSIP('Demand_Forecast')

#We put it in a pandas dataframe to make the vector math simpler
df = pd.DataFrame(demand_sip, columns=["simulation"])

#Calculating our new revenue/profit based on our uncertainty
df["production decision"] = production_decision
cost = cost_per_unit * production_decision
print("Cost: "+str(cost))
revenue = price_per_unit * df[['simulation','production decision']].min(axis=1)
print("Potential Revenues")
print(revenue[:10])
profit = revenue - cost
print("Potential Profits")
print(profit[:10])

#The revenue and profit variables can be used in simulations or summarized
mean(profit)