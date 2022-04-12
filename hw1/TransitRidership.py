# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 16:57:09 2022

@author: f001q00
"""

#import os
from gurobipy import Model, GRB
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

#Data
cost_per_trip = [400, 125, 60, 40]
ridership_per_trip = [200, 80, 40, 30]
cost_budget = 5000
Modes = ["heavy_rail", "light_rail", "brt", "bus"]


#Model
m = Model("ridership")
trips = m.addVars(
    Modes, 
    vtype=GRB.CONTINUOUS, 
    obj=cost_per_trip, 
    name="Trips")
m.modelSense = GRB.MAXIMIZE
m.addConstr(
    sum(ridership_per_trip[i] * trips[mode] for i, mode in enumerate(Modes)) <= cost_budget,
    name="Budget")

m.optimize()

#Print Results
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

    