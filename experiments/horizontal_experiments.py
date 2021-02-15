import os
import sys
import time
from pathlib import Path

import pandas as pd
from urinterface.robot_connection import RobotConnection

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Import paths from parents directory
from plates.plateA import *
from plates.plateP import *
from screwdriver_utils import screwdriver
from utils import *

# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# -----------------------------Experiment utility -------------------------------

def get_horizontal_from_and_to_arrays(from_plate, to_plate):
    if from_plate == "P" or from_plate == "p":
        from_array_values = p_horizontal_movement
        to_array_values = a_horizontal_movement
        from_array_pins = p_horizontal_pins
        to_array_pins = a_horizontal_pins
    else:
        from_array_values = a_horizontal_movement
        to_array_values = p_horizontal_movement
        from_array_pins = a_horizontal_pins
        to_array_pins = p_horizontal_pins
    assert len(from_array_values) == len(to_array_values), f"The number of points in each plate do not correspond, from plate {from_plate} length is {len(from_array_values)}, and to plate {to_plate} length is {len(to_array_values)}"
    assert len(to_array_values) == len(to_array_pins), f"The length of the to plate points ({len(to_array_values)}) is not equal to the length of the to array pins ({len(to_array_pins)})"
    
    return from_array_values, to_array_values, to_array_pins, from_array_pins



# ---------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------
# -------------------- Run Horizontal Experiment functions ----------------------------


def run_normal_horizontal(from_plate, to_plate, start_N):
    folder = Path("test_results") / Path("horizontal_normal")
    filename = get_save_filename(folder, from_plate, to_plate)
    from_array_values, to_array_values, to_array_pins, from_array_pins = get_horizontal_from_and_to_arrays(from_plate, to_plate)
    # Create screwdriver instance
    sd = setup_and_get_sd(folder, filename)

    sd.start()
    time.sleep(1)

    vel = 2.0
    acc = 1.0
    
    sd.move_home_bool(home_pos, vel, acc)

    N = len(from_array_values)
    for i in range(start_N,N):
        sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i], from_array_pins[i])


    sd.stop()

    load_screw_test_program(sd)

    save_data_with_anomalies(folder, filename, [], "", from_array_pins, to_array_pins, label_loosen=True)