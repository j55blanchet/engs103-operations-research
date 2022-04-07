# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 17:26:09 2022

@author: f001q00
"""

#import os
from gurobipy import Model, GRB
#import scipy as sp
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

#Data
c = [400, 500, 300, 150]
t = [(20, 40, 50), (48, 15, 26), (26, 35, 18), (24, 50, 35)]
Cities = range(4)
Regions = range(3)
Fixed = [400, 500, 300, 150]
Demands = [80, 70, 40]
Cap = 100

#Model
m = Model("warehouse")
x = m.addVars(Cities, Regions, vtype=GRB.CONTINUOUS, obj=t, name="Flow")
y = m.addVars(Cities, vtype=GRB.BINARY, obj=c, name="Open")
m.modelSense = GRB.MINIMIZE

m.addConstrs(
    (x.sum(city,'*') <= Cap*y[city] for city in Cities),
    name="Forcing")
m.addConstrs(
    (x.sum('*',region) == Demands[region] for region in Regions),
    name="Demand")

m.optimize()


#Print Results
for v in m.getVars():
    print('%s %g' % (v.varName, v.x))

print('Obj: %g' % m.objVal)
