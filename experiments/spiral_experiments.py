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


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# -----------------------------Experiment utility -------------------------------

def get_spiral_from_and_to_arrays(from_plate, to_plate):
    if from_plate == "P" or from_plate == "p":
        from_array_values = p_spiral_movement
        to_array_values = a_spiral_movement
        from_array_pins = p_spiral_pins
        to_array_pins = a_spiral_pins
    else:
        from_array_values = a_spiral_movement
        to_array_values = p_spiral_movement
        from_array_pins = a_spiral_pins
        to_array_pins = p_spiral_pins
    assert len(from_array_values) == len(
        to_array_values), f"The number of points in each plate do not correspond, from plate {from_plate} length is {len(from_array_values)}, and to plate {to_plate} length is {len(to_array_values)}"
    assert len(to_array_values) == len(
        to_array_pins), f"The length of the to plate points ({len(to_array_values)}) is not equal to the length of the to array pins ({len(to_array_pins)})"

    return from_array_values, to_array_values, to_array_pins, from_array_pins


def get_anomaly_spiral(from_plate, to_plate, anomaly_name):
    folder = Path("test_results") / Path("spiral_" + anomaly_name)
    filename = get_save_filename(folder, from_plate, to_plate)
    # Create screwdriver instance
    sd = setup_and_get_sd(folder, filename)
    from_array_values, to_array_values, to_array_pins, from_array_pins = get_spiral_from_and_to_arrays(from_plate,
                                                                                                       to_plate)

    return from_array_values, to_array_values, to_array_pins, from_array_pins, folder, filename, sd


# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# -------------------- Run SPIRAL Experiment functions ----------------------------


def run_normal_spiral(from_plate, to_plate, include_starting_point, include_every_n_points, start_N):
    folder = Path("test_results") / Path("spiral_normal")
    filename = get_save_filename(folder, from_plate, to_plate)
    # Create screwdriver instance
    sd = setup_and_get_sd(folder, filename)
    from_array_values, to_array_values, to_array_pins, from_array_pins = get_spiral_from_and_to_arrays(from_plate,
                                                                                                       to_plate)

    # Skip every nth pin starting from the include_starting_point pin
    included_pins_to = include_every_N_points_from(to_array_pins, include_every_n_points, include_starting_point)
    included_pins_from = include_every_N_points_from(from_array_pins, include_every_n_points, include_starting_point)

    print(f'skipped pins are: {included_pins_from}')

    # Skip every nth point value starting from the include_starting_point value
    included_values_to = include_every_N_points_from(to_array_values, include_every_n_points, include_starting_point)
    included_values_from = include_every_N_points_from(from_array_values, include_every_n_points,
                                                       include_starting_point)

    sd.start()
    time.sleep(1)

    vel = 2.0
    acc = 1.0

    sd.move_home_bool(home_pos, vel, acc)

    N = len(included_pins_from)
    N = 20
    for i in range(start_N, N):
        sd.screw_motion(vel, acc, home_pos, included_values_from[i], included_values_to[i], included_pins_to[i],
                        included_pins_from[i])
        save_points(included_pins_from[i], included_pins_to[i])

    sd.stop()

    load_screw_test_program(sd)

    # save_data_with_anomalies(folder, filename, [], "", from_array_pins, to_array_pins, label_loosen=True)


def run_missing_screw_spiral(from_plate, to_plate, include_starting_point, include_every_n_points, start_N, mode):
    anomaly_name = "missing_screw"
    from_array_values, to_array_values, to_array_pins, from_array_pins, folder, filename, sd = get_anomaly_spiral(
        from_plate, to_plate, anomaly_name)

    if mode == 'skip':
        missing_screw_pins = include_every_N_points_from(to_array_pins, include_every_n_points, include_starting_point)
    elif mode == 'random':
        missing_screw_pins = create_random_anomalies(to_array_pins=to_array_pins, n_anomalies=46)

    print(f'Anomalies are: {missing_screw_pins}')

    # save anomalies to file
    path_name = Path(folder) / Path("missing_screw_pins.txt")
    with open(path_name, 'w') as f:
        f.write(f"{missing_screw_pins}\n")

    sd.start()
    time.sleep(1)

    vel = 2.0
    acc = 1.0

    sd.move_home_bool(home_pos, vel, acc)

    N = len(from_array_values)
    for i in range(start_N, N):
        if to_array_pins[i] in missing_screw_pins:
            sd.missing_screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i],
                                    from_array_pins[i])
        else:
            sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i],
                            from_array_pins[i])
        save_points(from_array_pins[i], to_array_pins[i])

    sd.stop()

    load_screw_test_program(sd)

    # save_data_with_anomalies(folder, filename, missing_screw_pins, anomaly_name, from_array_pins, to_array_pins,
    #                          label_loosen=True)


def run_extra_assembly_comp_spiral(from_plate, to_plate, include_every_n_points, include_starting_point, start_N, mode):
    anomaly_name = "extra_assembly_comp"
    from_array_values, to_array_values, to_array_pins, from_array_pins, folder, filename, sd = get_anomaly_spiral(
        from_plate, to_plate, anomaly_name)

    if mode == 'skip':
        extra_assembly_comp_pins = include_every_N_points_from(to_array_pins, include_every_n_points,
                                                               include_starting_point)
    elif mode == 'random':
        extra_assembly_comp_pins = create_random_anomalies(to_array_pins=to_array_pins, n_anomalies=25)
        print(f'The pins with extra assembly component are:{extra_assembly_comp_pins}')

    # save anomalies to file
    path_name = Path(folder) / Path("spiral_extra_assembly_comp.txt")
    with open(path_name, 'w') as f:
        f.write(f"{extra_assembly_comp_pins}\n")

    sd.start()
    time.sleep(1)

    vel = 2.0
    acc = 1.0

    sd.move_home_bool(home_pos, vel, acc)

    N = len(from_array_values)
    for i in range(start_N, N):
        sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i],
                        from_array_pins[i])
        save_points(from_array_pins[i], to_array_pins[i])

    sd.stop()

    load_screw_test_program(sd)

    # save_data_with_anomalies(folder, filename, extra_assembly_comp_pins, anomaly_name, from_array_pins, to_array_pins,
    #                          label_loosen=True)


def run_damaged_screw_thread_spiral(from_plate, to_plate, include_every_n_points, include_starting_point, start_N,
                                    mode):
    anomaly_name = "damaged_screw_thread"
    from_array_values, to_array_values, to_array_pins, from_array_pins, folder, filename, sd = get_anomaly_spiral(
        from_plate, to_plate, anomaly_name)

    if mode == 'skip':
        damaged_screw_thread_pins = include_every_N_points_from(to_array_pins, include_every_n_points,
                                                                include_starting_point)
    elif mode == 'random':
        damaged_screw_thread_pins = create_random_anomalies(to_array_pins=to_array_pins, n_anomalies=10, seed_source=4)
        print(f'The pins with damaged thread are:{damaged_screw_thread_pins}')

    from_array_values, from_array_pins = join_plates(damaged_screw_thread_pins, from_array_values, from_array_pins,
                                                     to_array_pins, [c1, c2, c3, c4, c5, c6, c7, c8, c9,
                                                                     c10])  # to_anomalies, original_from_plate, original_from_pins, to_pins, exchange_points

    # save anomalies to file
    path_name = Path(folder) / Path("damaged_screw_thread_pins.txt")
    with open(path_name, 'w') as f:
        f.write(f"{damaged_screw_thread_pins}\n")

    sd.start()
    time.sleep(1)

    vel = 2.0
    acc = 1.0

    sd.move_home_bool(home_pos, vel, acc)

    N = len(from_array_values)
    for i in range(start_N, N):
        if to_array_pins[i] in damaged_screw_thread_pins:
            sd.damaged_screw_thread_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i],
                                           to_array_pins[i], from_array_pins[i])
        else:
            sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i],
                            from_array_pins[i])
        save_points(from_array_pins[i], to_array_pins[i])

    sd.stop()

    load_screw_test_program(sd)

    # save_data_with_anomalies(folder, filename, damaged_screw_thread_pins, anomaly_name, from_array_pins, to_array_pins,
    #                          label_loosen=True)
