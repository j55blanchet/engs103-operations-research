


import math

def solve_airline_problem(
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
    flights_offered_convergence_tolerance = 0,
    verbose=True,
):
    # Copying to new arrays
    x = [xi for xi in xi_airline_initial_flights]
    s = [si for si in si_airline_initial_aircraft]

    operating_costs = [
        operating_cost_base + operating_cost_per_seat * seats
        for seats in aircraft_sizes
    ]
    min_profitable_passengers_by_flight_capacity = [
        cost / p_ticket_fare
        for cost in operating_costs   
    ]
    max_profitable_flights_by_aircraft_size = [
        m_market_size / min_passengers
        for min_passengers in min_profitable_passengers_by_flight_capacity
    ]
    max_flights_to_consider_offering = max(max_profitable_flights_by_aircraft_size)

    def calculate_market_share(i, xi=None):
        # other_sum = sum(x) - x[i]
        if xi is None:
            xi = x[i]
        x_squared = [pow(v, 1.5) for v in x[:i]] + [pow(xi, 1.5)] + [pow(v, 1.5) for v in x[i+1:]]
        demon = sum(x_squared)
        return 0.0 if demon == 0 else (pow(xi, 1.5) / demon)

    def calculate_profit(i, xi=None, si=None, market_share=None):
        if xi is None:
            xi = x[i]
        if si is None:
            si = s[i]
        if market_share is None:
            market_share = calculate_market_share(i, xi)

        max_capacity_passengers = xi_candidate * s_aircraft_size_candidate
        max_market_passengers = math.floor(market_share * m_market_size)
        passengers = min(max_capacity_passengers, max_market_passengers)
        return passengers * p_ticket_fare - xi * (operating_cost_base + (operating_cost_per_seat * si))

    def print_status(indent=""):
        for i in range(len(x)):
            print(f"{indent}Airlines {i+1} - flights={x[i]}, capacity={s[i]}, market share={100 * calculate_market_share(i):.1}%, profit=${calculate_profit(i) / 1000:.2f}k")

    for iteration_i in range(iterations_max):
        net_decision_deviation = 0
        if verbose:
            print(f"\tIteration {iteration_i + 1}")

        for i_airline in range(len(x)):

            max_profit = -math.inf
            chosen_si_aircraft_size = 0
            chosen_xi_flights_offered = 0

            for xi_candidate in range(math.ceil(max_flights_to_consider_offering)):
                market_share = calculate_market_share(i_airline, xi_candidate)
                xi_profit = -math.inf
                xi_si = 0
                for s_aircraft_size_candidate in aircraft_sizes:
                    profit = calculate_profit(i_airline, xi_candidate, s_aircraft_size_candidate, market_share)
                    if profit > max_profit:
                        max_profit = profit
                        chosen_si_aircraft_size = s_aircraft_size_candidate
                        chosen_xi_flights_offered = xi_candidate
                    if profit > xi_profit:
                        xi_profit = profit
                        xi_si = s_aircraft_size_candidate
                
                # print(f"\t\t\tAirline {i_airline + 1}: {xi_candidate=} si:{xi_si}  profit:${xi_profit / 1000.0:.1f}k,  market share:{market_share:.2%}" + ("  ⭐️" if chosen_xi_flights_offered==xi_candidate else ""))

            prev_flights = x[i_airline]
            prev_aircraft_size = s[i_airline]

            decision_deviation_flights = abs(prev_flights - chosen_xi_flights_offered)
            decision_deviation_capacity = abs(chosen_si_aircraft_size - prev_aircraft_size)
            decision_deviation = decision_deviation_flights + decision_deviation_capacity

            if decision_deviation > 0:
                if verbose:
                    print(f"\t\tAirline {i_airline + 1}", end="")
                    if decision_deviation_flights > 0:
                        print(f" changed flights {prev_flights}=>{chosen_xi_flights_offered}, ", end="")
                    else:
                        print(f" remained at {chosen_xi_flights_offered} flights, ", end="")

                    if decision_deviation_capacity > 0:
                        print(f"changed capacity {prev_aircraft_size}=>{chosen_si_aircraft_size}.", end="")
                    else:
                        print(f"remained at {chosen_si_aircraft_size} plane capacity.", end="")

                old_market_share = calculate_market_share(i_airline)
                new_market_share = calculate_market_share(i_airline, chosen_xi_flights_offered)
                if verbose:
                    print(f" Market share {100 * old_market_share:.0f}% => {100 *new_market_share:.0f}%.", end="")
                    print(" Profit: ${:.2f}k".format(max_profit / 1000))

            net_decision_deviation += decision_deviation
            x[i_airline] = chosen_xi_flights_offered
            s[i_airline] = chosen_si_aircraft_size
        
        if net_decision_deviation <= flights_offered_convergence_tolerance:
            print(f"\t\t == Converged == ({iteration_i+1} iterations)")
            if not verbose:
                print_status("\t")
            return x, s, True

        elif verbose:
            print("\t\t\tCurrent Status:")
            print_status("\t\t")
    
    print(f"\tDid not converge after {iterations_max} iterations.")
    print_status("\t")
    return x, s, False

solve_airline_problem()
print("👆 base problem. Starting values: x=(0, 0), s=(100, 100)")
print()

for i, (x_start, s_start) in enumerate([
    ([5, 5], [100, 100]),
    ([5, 5], [80, 80]),
    ([5, 5], [120, 120]),

    ([3, 3], [100, 100]),
    ([1, 9], [100, 100]),
    ([2, 8], [100, 100]),
    ([10, 10], [100, 100]),
    ([12, 8], [100, 100]),


    ([23, 23], [120, 120]),
    ([15, 15], [80, 80]),
]):
    
    print(f"👇 Variation {i+1}: Starting values: {x_start=}, {s_start=}")
    solve_airline_problem(
        xi_airline_initial_flights = x_start,
        si_airline_initial_aircraft = s_start,
        verbose=False,
    )
    print()
    print()
    