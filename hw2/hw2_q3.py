# -*- coding: utf-8 -*-
"""
Created on Monday April 18 2022

@author: Julien Blanchet
"""

#import os
from itertools import product
from typing import *
from gurobipy import Model, GRB
import gurobipy as gp
from operator import mul, add

#import pandas as pd
#import numpy as np
#import matplotlib.pyplot as plt

#Data

iteration_count = 0
cur_best_obj = 0
cur_best_vars = []
cur_best_iteration = -1

def solve_ner_goalkeeping_linear(
    goal_keepers: List[str] = ['DO', 'JB', 'BR', 'JG', 'LJ'],
    salaries: List[float] =   [5, 3, 3.5, 4.5, 2],
    salary_cap: float = 8.0,
    purchase_prices: List[float] = [4.5, 6.5, 3, 4, 0],
    purchase_budget: float = 10.0,
    anticipated_values: List[float] = [10, 7, 5, 8, 3],
    pinned_values: Optional[List[Union[float, None]]] = [None, None, None, None, None],
):
    global iteration_count, cur_best_obj, cur_best_vars, cur_best_iteration
    iteration_count += 1
    
    env = gp.Env(empty=True)
    env.setParam('OutputFlag', 0)
    env.start()

    m = Model("Goalkeeping Linear", env=env)

    pinned_values = [None for _ in goal_keepers] if pinned_values is None else pinned_values

    goal_keepers_hires = m.addVars(
        goal_keepers,
        vtype=GRB.CONTINUOUS,
        lb=[
            0.0 if pinned_val is None else pinned_val
            for pinned_val in pinned_values
        ],
        ub=[
            1.0 if pinned_val is None else pinned_val
            for pinned_val in pinned_values
        ],
        obj=anticipated_values,
        name="Keepers"
    )
    m.modelSense = GRB.MAXIMIZE

    m.addConstr(
        sum([
            goal_keepers_hires[goal_keeper] * salary 
            for goal_keeper, salary 
            in zip(goal_keepers_hires, salaries)
        ]) <= salary_cap,
        name="Salary Cap"
    )

    m.addConstr(
        sum([
            goal_keepers_hires[goal_keeper] * purchase_price
            for goal_keeper, purchase_price
            in zip(goal_keepers_hires, purchase_prices)
        ]) <= purchase_budget,
        name="Purchase Budget"
    )

    m.optimize()

    print("\nIteration 🔄: ", iteration_count)

    is_infeasible = m.status == GRB.INFEASIBLE
    
    var_names = " ".join([v.varName.ljust(12) for v in m.getVars()])
    print(f"Variables:      {var_names}")

    pinned_strs = [f"{x:.4}" if x is not None else "_" for x in pinned_values]
    pv_str = ' '.join([pinned_str.ljust(12) for pinned_str in pinned_strs])
    print(f"Pinned Values:  {pv_str}")

    if is_infeasible:
        print("Model is infeasible")
        return

    var_values = " ".join([f"{v.x:.4}".ljust(12) for v in m.getVars()])
    print(f"Values:         {var_values}")
    
    print(f'Objective (Goals): {m.objVal:.4}')

    salary = sum([
        goal_keepers_hires[goal_keeper].x * salary
        for goal_keeper, salary
        in zip(goal_keepers_hires, salaries)
    ])
    purchase_price = sum([
        goal_keepers_hires[goal_keeper].x * purchase_price
        for goal_keeper, purchase_price
        in zip(goal_keepers_hires, purchase_prices)
    ])
    print(f'Total Salary: {salary:.4} (cap: {salary_cap:.4})')
    print(f'Purchase Price: {purchase_price:.4} (budget: {purchase_budget:.4})')

    is_integer = all([v.x.is_integer() for v in m.getVars()])

    if is_integer and m.objVal > cur_best_obj:
        cur_best_obj = m.objVal
        cur_best_vars = [v.x for v in m.getVars()]
        cur_best_iteration = iteration_count
        print(f"🌟 Model has integer solution with current best value: {cur_best_obj:.4}")
    elif is_integer and m.objVal == cur_best_obj:
        print(f"⭐️ Model has integer solution that ties previous best from iteration {cur_best_iteration}")
    elif is_integer:
        print(f"✨ Model has an integer solution, however current best score (of {cur_best_obj:.4}, from iteration {cur_best_iteration}) is not improved.")

    return m

solve_ner_goalkeeping_linear(pinned_values=[None,  1.0, None, None, None]) # Iteration 1
solve_ner_goalkeeping_linear(pinned_values=[None,  1.0, None, None, None]) # Iteration 2
solve_ner_goalkeeping_linear(pinned_values=[None,  0.0, None, None, None]) # Iteration 3
solve_ner_goalkeeping_linear(pinned_values=[None,  1.0, None, None, 1.0])  # Iteration 4
solve_ner_goalkeeping_linear(pinned_values=[None,  1.0, None, None, 0.0])  # Iteration 5
solve_ner_goalkeeping_linear(pinned_values=[1.0,   1.0, None, None, 1.0])  # Iteration 6: Infeasible
solve_ner_goalkeeping_linear(pinned_values=[0.0,   1.0, None, None, 1.0])  # Iteration 7
solve_ner_goalkeeping_linear(pinned_values=[None,  0.0, None, 1.0,  None]) # Iteration 8
solve_ner_goalkeeping_linear(pinned_values=[None,  0.0, None, 0.0,  None]) # Iteration 9
solve_ner_goalkeeping_linear(pinned_values=[1.0,   0.0, None, 1.0,  None]) # Iteration 10: Infeasible
solve_ner_goalkeeping_linear(pinned_values=[0.0,   0.0, None, 1.0,  None]) # Iteration 11
solve_ner_goalkeeping_linear(pinned_values=[1.0,   1.0, None, None, 0.0])  # Iteration 12: Infeasible
solve_ner_goalkeeping_linear(pinned_values=[0.0,   1.0, None, None, 0.0])  # Iteration 13
solve_ner_goalkeeping_linear(pinned_values=[0.0,   1.0, None, 1.0, 0.0])   # Iteration 14: Infeasible
solve_ner_goalkeeping_linear(pinned_values=[0.0,   1.0, None, 0.0, 0.0])   # Iteration 15: A new best integer solution!

solve_ner_goalkeeping_linear(pinned_values=[None,  0.0, 1.0, 0.0, None])   # Iteration 16
solve_ner_goalkeeping_linear(pinned_values=[None,  0.0, 0.0, 0.0, None])   # Iteration 17: A new best integer solution!

solve_ner_goalkeeping_linear(pinned_values=[1.0,  0.0, 1.0, 0.0, None])   # Iteration 18
solve_ner_goalkeeping_linear(pinned_values=[0.0,  0.0, 1.0, 0.0, None])   # Iteration 19: A suboptimal integer solution

solve_ner_goalkeeping_linear(pinned_values=[0.0,  1.0, None, 1.0, 1.0])   # Iteration 20: Infeasible
solve_ner_goalkeeping_linear(pinned_values=[0.0,  1.0, None, 0.0, 1.0])   # Iteration 21

solve_ner_goalkeeping_linear(pinned_values=[0.0,  1.0, 1.0, 0.0, 1.0])   # Iteration 22: Infeasible
solve_ner_goalkeeping_linear(pinned_values=[0.0,  1.0, 0.0, 0.0, 1.0])   # Iteration 23: A suboptimal integer solution


solve_ner_goalkeeping_linear(pinned_values=[0.0,  0.0, 0.0, 1.0, None]) # Iteration 24: A suboptimal integer solution
solve_ner_goalkeeping_linear(pinned_values=[0.0,  0.0, 1.0, 1.0, None]) # Iteration 25: A suboptimal integer solution