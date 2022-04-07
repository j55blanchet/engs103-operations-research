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
c = [400, 125, 60, 40]
A = [200, 80, 40, 30]
b = 5000
Modes = range(4)

#Model
m = Model("ridership")
trips = m.addVars(Modes, vtype=GRB.CONTINUOUS, obj=c, name="Trips")
m.modelSense = GRB.MAXIMIZE
m.addConstr(
    sum(A[mode] * trips[mode] for mode in Modes) <= b,
    name="Budget")

m.optimize()

#Print Results
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)

    