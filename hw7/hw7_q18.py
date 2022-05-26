


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
):
    # Copying to new arrays
    xi = [x for x in xi_airline_initial_flights]
    si = [s for s in si_airline_initial_aircraft]

    pass