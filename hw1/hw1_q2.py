import math
from typing import *
from webbrowser import UnixBrowser
from gurobipy import Model, GRB
import numpy as np

def solve_vitamin_composition_problem(
    ingredients: List[str],
    vitamins: List[str],
    upper_bounds: List[float],
    ingredient_vitamin_compositions: np.ndarray,
    vitamin_requirements: List[float],
    ingredient_calories: List[float],
):


    m = Model('Vitamin Pill Composition')

    ingredient_usage_quantities = m.addVars(
        ingredients,
        vtype=GRB.CONTINUOUS,
        lb=0.0,
        ub=upper_bounds,
        obj=ingredient_calories,
        name='Ingredient Usage Quantities',
    )
    m.modelSense = GRB.MINIMIZE

    for i, vit_name in enumerate(vitamins):
        m.addConstr(
            sum(
                ingredient_vitamin_compositions[j, i] * ingredient_usage_quantities[ing_name] 
                for j, ing_name in enumerate(ingredients)
            ) >= vitamin_requirements[i],
            name=f'Vitamin {vit_name} Requirement',
        )

    m.optimize()

    print()

    print('Objective (Calories): %g' % m.objVal)

    duals = []
    for i, vit_name in enumerate(vitamins):
        val = sum(
            ingredient_vitamin_compositions[j, i] * ingredient_usage_quantities[ing_name].x 
            for j, ing_name in enumerate(ingredients)
        )
        dual = m.getConstrByName(f'Vitamin {vit_name} Requirement').Pi
        duals.append(dual)
        print(f'Constraint - {vit_name}: {val} (dual: {dual})')

    for v in m.getVars():
        # reduced_cost = v.RC
        print('%s %g (reduced cost: %g)' % (v.varName, v.x, v.RC))
    return m


solve_vitamin_composition_problem(
    ingredients=['Ingredient-'+str(i) for i in range(1, 6)],
    upper_bounds=math.inf,
    vitamins=['Vitamin A', 'Vitamin B', 'Vitamin C'],
    ingredient_vitamin_compositions=np.array([
        [17.0, 13.0, 19.0],
        [9.0, 4.0, 9.0],
        [8.0, 30.0, 4.0],
        [7.0, 8.0, 17.0],
        [26.0, 18.0, 6.0]
    ]),
    vitamin_requirements=[
        1000.0, 1000.0, 1000.0,
    ],
    ingredient_calories=[
        56.0, 29.0, 35.0, 25.0, 47.0
    ],
)
print('☝️part a')


print('\n\n')
solve_vitamin_composition_problem(
    ingredients=['Ingredient-'+str(i) for i in range(1, 6)],
    upper_bounds=[math.inf, math.inf, math.inf, 15, math.inf],
    vitamins=['Vitamin A', 'Vitamin B', 'Vitamin C'],
    ingredient_vitamin_compositions=np.array([
        [17.0, 13.0, 19.0],
        [9.0, 4.0, 9.0],
        [8.0, 30.0, 4.0],
        [7.0, 8.0, 17.0],
        [26.0, 18.0, 6.0]
    ]),
    vitamin_requirements=[
        1000.0, 1000.0, 1000.0,
    ],
    ingredient_calories=[
        56.0, 29.0, 35.0, 25.0, 47.0
    ],
)
print('☝️part b')