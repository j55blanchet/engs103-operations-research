"""
    Homework 6
    Question 14

    Author: Julien Blanchet
    Date: 2022-05-23

    Hospital Radiology Department Simulation. 
    
    Goal: Analyze the workflow of a radiology department to make suggestions for improvements.
"""
# %%
# Part (b)

from typing import Callable
import numpy as np
import math
import numpy.random as npr

rng = npr.default_rng()


def run_radiology_dept_sim(
    n_patients: int = 10000,
    w_warmup: int = 100,

    scheduled_arrival_func: Callable[[int], float]
    = lambda i: i * 30,
    arrival_time_func: Callable[[float], float] 
        = lambda scheduled_arrival: scheduled_arrival + rng.uniform(-10, 10),
    consent_finished_func: Callable[[float], float] 
        = lambda arrive_time: 
            arrive_time + (2 if rng.random() < 0.8 else 10),
    patient_prepstart_func: Callable[[float, float], float]
        = lambda consent_finished, prev_exam_finished:
            max(consent_finished, prev_exam_finished),
    patient_prepped_func: Callable[[float], float]
        = lambda prep_started:
            prep_started - math.log(rng.random())* 15, #rng.exponential(15.0),
    room_prepped_func: Callable[[float], float]
        = lambda prev_exam_finished:
            prev_exam_finished + 10,
    exam_started_func: Callable[[float, float], float]
        = lambda patient_prepped, room_prepped: 
            max(patient_prepped, room_prepped) ,
    exam_finished_func: Callable[[float], float] 
        = lambda exam_started: 
            exam_started + 
                (8 if rng.random() < (1/3.0) else 
                    (10 if rng.random() < 0.5 else 12)
                ),
):
    """Run a simulation of the radiology department

    Args:
        n_patients (int, optional): Number of patients to simulate. 
            Defaults to 1000.
        w_warmup (int, optional): Warmup period to skip for statistics calculation. 
            Defaults to 100.
        scheduled_arrival_func(Callable[[int], float], optional): Function that calculates the scheduled arrival time of 
            a patient. Defaults to i * 30 min.
        arrival_time_func (Callable[[float], float], optional): Function to calculates the actual arrival time of a patient. 
            Defaults to scheduled_arrival + uniform(-10, 10).
        consent_finished_func (Callable[[float], float], optional): Function to calculate the consent time of a patient. 
            Defaults to arrive_time + 2 minutes (80% of the time) or 10 mins (20% of the time).
        patient_prepstart_func (Callable[[float, float], float], optional): Function to calculate the time when a patient
            starts preparing for an exam. Defaults to max(consent_finished, prev_exam_finished).
        patient_prepped_func (Callable[[ float], float], optional): Function to calculate the time at which a patient 
            is prepared for the exam. Takes (prep_started) as input.  
            Defaults to prep_started + exponential(lambda=15.0).'
        room_prepped_func (Callable[[float], float], optional): Function to calculate the time at which the exam room is 
            prepared for a patient. Takes (prev_exam_finished) as input. Defaults to prev_exam_finished + 10.
        exam_finished_func (Callable[[float, float, float], optional): Function to calculate when a patient's exam is 
            finished. Takes (patient_prepped, room_prepped) as inputs. 
            Defaults to max(patient_prepped, room_prepped) + (8, 10, or 12 mins with equal probability).
    """

    values = np.zeros((8, n_patients))

    scheduled_arrival_index = 0
    arrival_time_index = 1
    consent_time_index = 2
    patient_prepstart_index = 3
    patient_prepped_index = 4
    room_prepped_index = 5
    exam_started_index = 6
    exam_finished_index = 7
    
    prev_patient_finish_time = 0
    for i in range(n_patients):
        scheduled_arrival = scheduled_arrival_func(i)
        values[scheduled_arrival_index][i] = scheduled_arrival
        
        arrival_time = arrival_time_func(scheduled_arrival)
        values[arrival_time_index ][i] = arrival_time

        consent_finished_time = consent_finished_func(arrival_time)
        values[consent_time_index ][i] = consent_finished_time

        patient_prepstart_time = patient_prepstart_func(consent_finished_time, prev_patient_finish_time)
        values[patient_prepstart_index][i] = patient_prepstart_time

        patient_prepped_time = patient_prepped_func(patient_prepstart_time)
        values[patient_prepped_index][i] = patient_prepped_time

        room_prepped_time = room_prepped_func(prev_patient_finish_time)
        values[room_prepped_index ][i] = room_prepped_time

        exam_started_time = exam_started_func(patient_prepped_time, room_prepped_time)
        values[exam_started_index][i] = exam_started_time

        exam_finished_time = exam_finished_func(exam_started_time)
        values[exam_finished_index][i] = exam_finished_time

        prev_patient_finish_time = exam_finished_time
        

    # print("Finished")
    stats_vals = values[:, w_warmup:]

    avg_time = np.mean(stats_vals[exam_finished_index] - stats_vals[arrival_time_index])
    avg_time_from_scheduled = np.mean(stats_vals[exam_finished_index] - stats_vals[scheduled_arrival_index])

    total_examinprogress_time = np.sum(
        stats_vals[exam_finished_index] - stats_vals[exam_started_index]
    )
    total_examroomprep_time = np.sum(
        stats_vals[room_prepped_index, 1:] - stats_vals[exam_finished_index, :-1]
    )
    total_patientprep_time = np.sum(
        stats_vals[patient_prepped_index] - stats_vals[patient_prepstart_index]
    )

    total_time = stats_vals[exam_finished_index, -1] - stats_vals[consent_time_index, 0]
    
    examinprogress_percent = total_examinprogress_time / total_time
    examroomprep_percent = total_examroomprep_time / total_time
    patientprep_percent = total_patientprep_time / total_time

    # # Sanity checks
    # print("mean wait time waiting on exam room:", 
    #     np.mean(np.maximum(0, 
    #         stats_vals[exam_started_index] - stats_vals[patient_prepped_index]
    #     ))
    # )
    # print("mean wait time on prev patient:", np.mean(stats_vals[patient_prepstart_index] - stats_vals[consent_time_index]))
    # print("mean exam duration: ", np.mean(stats_vals[exam_finished_index] - stats_vals[exam_started_index]))
    # print("mean patient prep time: ", total_patientprep_time / (n_patients - w_warmup))
    # print("mean time exam room vacant: ", 
    #     np.mean(np.maximum(0,
    #         stats_vals[consent_time_index, 1:] - stats_vals[exam_finished_index, :-1]
    #     ))
    # )
    
    return avg_time, avg_time_from_scheduled, examinprogress_percent, examroomprep_percent, patientprep_percent

run_radiology_dept_sim()

# %%
# Part (c)

def run_multiple_sim(iterations, sim_func=run_radiology_dept_sim, print_intermediate=False):
    total_avg_time = 0 
    total_avg_time_from_scheduled = 0 
    total_examinprogress_percent = 0 
    total_examroomprep_percent = 0
    total_patientprep_percent = 0

    def print_stats(n, indent_str=""):
        avg_time = total_avg_time / n
        avg_time_from_scheduled = total_avg_time_from_scheduled / n
        examinprogress_percent = total_examinprogress_percent / n
        examroomprep_percent = total_examroomprep_percent / n
        patientprep_percent = total_patientprep_percent/ n

        print(f"{indent_str}Avg time spent per patient", avg_time)
        print(f"{indent_str}Avg time spent per patient (from scheduled arrival)", avg_time_from_scheduled)
        print(f"{indent_str}Percentage of time spent conducting exams", examinprogress_percent)
        print(f"{indent_str}Percentage of exam room time spent preparing the room:", examroomprep_percent)
        print(f"{indent_str}Percentage of time spent preparing the patient:", patientprep_percent)

    import time
    last_print = 0

    for i in range(iterations):
        vals = sim_func()
        total_avg_time += vals[0]
        total_avg_time_from_scheduled += vals[1]
        total_examinprogress_percent += vals[2]
        total_examroomprep_percent += vals[3]
        total_patientprep_percent += vals[4]

        if print_intermediate and time.time() - last_print > 3.0 and i > 0:
            percent = round(i / iterations * 100)
            print(f"{i}/{iterations} ({percent}%)")
            last_print = time.time()
            print_stats(i, f"    {i} ({percent}%): ")

        
    print("FINAL")
    print_stats(iterations)

run_multiple_sim(
    iterations=100_000,
    print_intermediate=True
)
# print("👆 part (c)")

# %%
# Part (d) - what if we call patients to ensure they arrive on time?

print()
print("Part d:")
run_multiple_sim(
    iterations=10000, 
    sim_func=lambda:
        run_radiology_dept_sim(
            arrival_time_func=lambda scheduled_arrival: scheduled_arrival,
        )
)


#%%
# Part (e) - what if we help patients fill out consent form?
print()
print("Part e:")
run_multiple_sim(
    iterations=10000, 
    sim_func=lambda:
        run_radiology_dept_sim(
            consent_finished_func=lambda arrive_time: arrive_time + 2,
        )
)
        


#%%
# Part (f) - what if we hire technician to prep exam room?
print()
print("Part f:")
run_multiple_sim(
    iterations=10000, 
    sim_func=lambda:
        run_radiology_dept_sim(
            room_prepped_func= lambda prev_exam_finished:
            prev_exam_finished + 5,
        )
)



#%%
# Part (g) - what if we build a new patient prep room?
print()
print("Part g:")
run_multiple_sim(
    iterations=10000, 
    sim_func=lambda:
        run_radiology_dept_sim(
            patient_prepstart_func=lambda consent_finished, prev_exam_finished: consent_finished,
        )
)
# %%
# Bonus
print()
print("Bonus: part g and f combined")
run_multiple_sim(
    iterations=1000, 
    sim_func=lambda:
        run_radiology_dept_sim(
            patient_prepstart_func=lambda consent_finished, prev_exam_finished: consent_finished,
            room_prepped_func= lambda prev_exam_finished: prev_exam_finished + 5,
        )
)
# %%
