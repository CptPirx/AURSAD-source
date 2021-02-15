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
from experiments.spiral_experiments import *
from experiments.horizontal_experiments import *
from experiments.seq_experiments import *


def get_experiment_names(scripts, script_dict):
    s = ""
    for i in range(len(scripts)):
        s += f"{scripts[i]}: {script_dict[scripts[i]]}\n"
    return s


if __name__ == "__main__":
    try:

        # Setup from plate to plate
        e1 = ["P", "A"]
        e2 = ["A", "P"]
        from_plate_to_plate = eval(input('e1 for P -> A, e2 for A -> P: '))
        print(f"\nProgram from plate {from_plate_to_plate[0]} to plate {from_plate_to_plate[1]}")

        points_from, points_to = load_saved_points()
        if points_to is None:
            n_points_to = 0
        else:
            n_points_to = len(points_to)
        print(f"n_points_to = {n_points_to}")

        # Ask for experiment to run
        scripts = ['sn', 'sms', 'seac', 'sdst', 'hn', 'seqdst']
        script_dict = {scripts[0]: 'Spiral Normal',
                       scripts[1]: 'Spiral Missing Screw',
                       scripts[2]: 'Spiral Extra Assembly Component',
                       scripts[3]: 'Spiral Damaged Screw Thread',
                       scripts[4]: 'Horizontal Normal',
                       scripts[5]: 'Sequential Damaged Screw Thread'}
        s = get_experiment_names(scripts, script_dict)
        input_string = f"Available possibilities:\n\n{s}\n\nPlease choose script: "
        script_name = input(input_string)
        while script_name not in scripts:
            print("The defined script is not available.\n")
            script_name = input(input_string)

        # Run chosen experiment
        print(
            f"Running script: {script_name} ({script_dict[script_name]}), from plate {from_plate_to_plate[0]} to plate {from_plate_to_plate[1]}")

        if script_name == scripts[0]:
            include_every_n_points = 4
            include_starting_point = 3
            run_normal_spiral(from_plate=from_plate_to_plate[0],
                              to_plate=from_plate_to_plate[1],
                              include_every_n_points=include_every_n_points,
                              include_starting_point=include_starting_point,
                              start_N=n_points_to)
        elif script_name == scripts[1]:
            include_every_n_points = 4
            skip_starting_point = 3
            run_missing_screw_spiral(from_plate=from_plate_to_plate[0],
                                     to_plate=from_plate_to_plate[1],
                                     include_every_n_points=include_every_n_points,
                                     include_starting_point=skip_starting_point,
                                     start_N=n_points_to,
                                     mode='skip')
        elif script_name == scripts[2]:
            include_every_n_points = 4
            skip_starting_point = 0
            run_extra_assembly_comp_spiral(from_plate_to_plate[0], from_plate_to_plate[1], include_every_n_points,
                                           skip_starting_point, n_points_to, mode='skip')
        elif script_name == scripts[3]:
            include_every_n_points = 4
            skip_starting_point = 3
            run_damaged_screw_thread_spiral(from_plate=from_plate_to_plate[0],
                                            to_plate=from_plate_to_plate[1],
                                            include_every_n_points=include_every_n_points,
                                            include_starting_point=skip_starting_point,
                                            start_N=n_points_to,
                                            mode='random')
        elif script_name == scripts[4]:
            run_normal_horizontal(from_plate_to_plate[0], from_plate_to_plate[1], n_points_to)
        elif script_name == scripts[5]:
            run_damaged_screw_thread_seq(from_plate_to_plate[0], from_plate_to_plate[1], 2, n_points_to)

    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting program\n")
        sys.exit(0)
