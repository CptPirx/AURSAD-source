
import os
import sys
import time
from pathlib import Path

import pandas as pd
from urinterface.robot_connection import RobotConnection

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Import paths from parents directory
from plates.plateA import *
from plates.plateP import *
from plates.plateC import *
from screwdriver_utils import screwdriver
from utils import *



def get_seq_from_and_to_arrays(from_plate, to_plate):
    if from_plate == "P" or from_plate == "p":
        from_array_values = p_seq_movement
        to_array_values = a_seq_movement
        from_array_pins = p_seq_pins
        to_array_pins = a_seq_pins
    else:
        from_array_values = a_seq_movement
        to_array_values = p_seq_movement
        from_array_pins = a_seq_pins
        to_array_pins = p_seq_pins
    assert len(from_array_values) == len(to_array_values), f"The number of points in each plate do not correspond, from plate {from_plate} length is {len(from_array_values)}, and to plate {to_plate} length is {len(to_array_values)}"
    assert len(to_array_values) == len(to_array_pins), f"The length of the to plate points ({len(to_array_values)}) is not equal to the length of the to array pins ({len(to_array_pins)})"
    
    return from_array_values, to_array_values, to_array_pins, from_array_pins


def get_anomaly_seq(from_plate, to_plate, anomaly_name):
    folder = Path("test_results") / Path("seq_" + anomaly_name)
    filename = get_save_filename(folder, from_plate, to_plate)
    # Create screwdriver instance
    sd = setup_and_get_sd(folder, filename)
    from_array_values, to_array_values, to_array_pins, from_array_pins = get_seq_from_and_to_arrays(from_plate, to_plate)
    
    return from_array_values, to_array_values, to_array_pins, from_array_pins, folder, filename, sd


def run_damaged_screw_thread_seq(from_plate, to_plate, include_every_n_points, start_N):
    anomaly_name = "damaged_screw_thread"
    from_array_values, to_array_values, to_array_pins, from_array_pins, folder, filename, sd = get_anomaly_seq(from_plate, to_plate, anomaly_name)
    damaged_screw_thread = include_every_N_points_from(to_array_pins,include_every_n_points)
    

    sd.start()
    time.sleep(1)

    vel = 2.0
    acc = 1.0

    sd.move_home_bool(home_pos, vel, acc)

    from_array_values, from_array_pins = join_plates(damaged_screw_thread, from_array_values, from_array_pins, to_array_pins, [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]) # to_anomalies, original_from_plate, original_from_pins, to_pins, exchange_points
    
    
    N = len(from_array_values)
    for i in range(start_N,N):
        if to_array_pins[i] in damaged_screw_thread:
            sd.damaged_screw_thread_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i], from_array_pins[i])
        else:
            sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i], from_array_pins[i])

    sd.stop()

    load_screw_test_program(sd)

    save_data_with_anomalies(folder, filename, damaged_screw_thread, anomaly_name, from_array_pins, to_array_pins, label_loosen=True)