


import math
from this import s


def solve_airline_problem(
    n_airlines = 2,
    xi_airline_initial_flights = [0, 0],
    si_airline_initial_aircraft = [100, 100],
    m_market_size = 1000,
    p_ticket_fare = 200,
    aircraft_sizes = [
        80,
        100,
        120,
    ],
    operating_cost_base = 2000,
    operating_cost_per_seat = 80,

    iterations_max = 1000,
):
    # Copying to new arrays
    xi = [x for x in xi_airline_initial_flights]
    si = [s for s in si_airline_initial_aircraft]

    operating_costs = [
        operating_cost_base + operating_cost_per_seat * seats
        for seats in aircraft_sizes
    ]
    min_passengers_per_flight = [
        cost / p_ticket_fare
        for cost in operating_costs   
    ]
    max_profitable_flights_by_aircraft_size = [
        m_market_size / min_passengers
        for min_passengers in min_passengers_per_flight
    ]
    max_flights_to_consider_offering = max(max_profitable_flights_by_aircraft_size)


    for iteration_i in range(iterations_max):
        for i_airline in range(n_airlines):
            max_profit = -math.inf
            chosen_aircraft_size = 0
            chosen_seats = 0

            flights_offered_by_other_airlines = sum(xi) - xi[i_airline]

            for xi_candidate in range(max_flights_to_consider_offering):
                market_share = pow(xi_candidate, 1.5) / \
                               pow(flights_offered_by_other_airlines + xi_candidate, 1.5)
                for s_aircraft_size_candiate in aircraft_sizes:

    pass