# -*- coding: utf-8 -*-
"""
Created on Tuesday April 12 2022

@author: Julien Blanchet
"""

#import os
from typing import *
from gurobipy import Model, GRB
#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

#Data

def solve_bakery_production_problem(
    products: List[str],
    demand: List[float],
    sell_price: List[float],
    butter_requirements: List[float],
    sugar_requirements: List[float],
    butter_unit_cost: float,
    sugar_unit_cost: float,
    butter_inventory: float,
    sugar_inventory: float,
):
    objective_coefficient = [
        -sell_price[i] + butter_unit_cost * butter_requirements[i] + sugar_unit_cost * sugar_requirements[i]
        for i, _ 
        in enumerate(products)
    ]

    #Model
    m = Model("bakery_production")
    product_production = m.addVars(
        products, 
        vtype=GRB.CONTINUOUS, 
        lb=0.0, 
        ub=demand,
        obj=objective_coefficient, 
        name="Baked Goods Production"
    )

    m.modelSense = GRB.MINIMIZE

    # Add sugar & butter constraints
    butter_constraint = sum(
            [butter_requirements[i] * 
            product_production[product_name] for i, product_name in enumerate(products)]
        ) <= butter_inventory

    m.addConstr(
        butter_constraint,
        name="Butter Inventory"
    )

    sugar_constraint = sum(
            [sugar_requirements[i] *
            product_production[product_name] for i, product_name in enumerate(products)]
        ) <= sugar_inventory

    m.addConstr(
        sugar_constraint,
        name="Sugar Inventory"
    )

    m.optimize()

    res_vars = m.getVars()
    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Objective: %g' % m.objVal)
    print('\tButter Used', sum((butter_requirements[i]*v.x for i, v in enumerate(res_vars))))
    print('\tSugar Used', sum((sugar_requirements[i]*v.x for i, v in enumerate(res_vars))))

    return m


solve_bakery_production_problem(
    products = ["muffins",  "pastries"],
    demand = [200, 80],
    sell_price = [3, 10],
    butter_requirements = [2, 5],
    sugar_requirements = [0.5, 2],

    butter_unit_cost = 0.5,
    sugar_unit_cost = 1.2,
    butter_inventory = 600,
    sugar_inventory = 300,
)
print("☝️ solution for q1 part (a)")

print('\n\n')

solve_bakery_production_problem(
    products = ["muffins",  "pastries", "candy"],
    demand = [200, 80, 99],
    sell_price = [3, 10, 5],
    butter_requirements = [2, 5, 0],
    sugar_requirements = [0.5, 2, 1],

    butter_unit_cost = 0.5,
    sugar_unit_cost = 1.2,
    butter_inventory = 600,
    sugar_inventory = 300,
)
print("☝️ solution for q1 part (e)")
#Print Results


    