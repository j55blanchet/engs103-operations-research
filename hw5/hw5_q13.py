"""
    Homework 5
    Question 13

    Author: Julien Blanchet
    Date: 2022-05-16

    Inventory managent simulation. 
    
    Goal: find the optimal integer value of constant P by trial and error so as
    to minimize the expected cost of backlog and storage.
"""

import numpy as np
import math
import numpy.random as npr

rng = npr.default_rng()

def run_inventory_management_sim(
    weeks: int = 1000,
    p_base_order: float = 100,
    starting_storage: float = 0,
    starting_backlog: float = 0,
    cost_per_unit_storage: float = 2,
    cost_per_unit_backlog: float = 3,
    demand_mean: float = 100,
    demand_stddev: float = 10,
    trial_number: int = 1,
    warmup_weeks: int = 100,
):
    total_cost = 0
    s_i = starting_storage
    b_i = starting_backlog
    
    for i in range(weeks):
        demand: float = rng.normal(demand_mean, demand_stddev)
        order = p_base_order - s_i + b_i

        s_i = max(0, demand - p_base_order)
        b_i = -min(0, demand - p_base_order)
        if order < 0:
            print(f"Trial {trial_number} Iteration {i+1} - Warning: order is negative {order}")

        if i >= warmup_weeks:
            total_cost += s_i * cost_per_unit_storage + b_i * cost_per_unit_backlog
    
    weeks_to_count = weeks - warmup_weeks
    return total_cost / weeks_to_count



costs = np.array([
    run_inventory_management_sim(
        trial_number=i+1,
        warmup_weeks=100,
        weeks=1000,
    )
    for i in range(1000)
])

print()
print("Part (b) - p=100, warmup=100, weeks=1000, iterations=1000")
print(f"Mean weekly cost: {np.mean(costs)}")
print(f"Std deviation: {np.std(costs)}")
print()


for p in [
    80, 
    90, 
    93,
    94,
    95,
    96,
    97,
    98,
    99, 
    100, 
    101,
    105, 
    110, 
]:
    costs = np.array([
        run_inventory_management_sim(
            trial_number=i+1,
            warmup_weeks=100,
            weeks=1000,
            p_base_order=p,
        )
        for i in range(1000)
    ])

    print(f"Part (c) - p={p:3} - mean weekly cost={np.mean(costs)}")
    
    
    
