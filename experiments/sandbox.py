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
import utils


def check_register(csv_filename, register):
    folder = "test_results"
    file_path = Path(folder) / Path(csv_filename)

    df = pd.read_csv(file_path, sep=" ")
    # Check if column exists
    if register not in df.columns:
        print(f"Error, the column {register} does not exist")
    else:
        register_output = df[register]
        # print(f"Unique values: {np.unique(register_output)}")
        print(f"N unique vals: {len(np.unique(register_output))}")
        print(f"max: {np.max(register_output)}")
        print(f"min: {np.min(register_output)}")
        # print(f"Values: {register_output}")


def run(csv_filename):
    # Define velocity and acceleration
    vel = 2.0
    acc = 1.0

    sd = screwdriver.Screwdriver()
    sd.set_filename_and_config(save_exp_dir=Path("test_results"), 
                                    config_file_dir=Path("resources"), 
                                    save_exp_filename=csv_filename, 
                                    config_filename="record_configuration.xml")
    sd.start()

    time.sleep(1)

    p_array = [p1, p2, p3]
    a_array = [a1, a2, a3]
    random_points1 = [a23, a9, a16]
    random_points2 = [p14, p17, p11]

    from_array_values = p_spiral_movement
    to_array_values = a_spiral_movement
    to_array_pins = a_spiral_pins
    from_array_pins = p_spiral_pins
    missing_screw_pins = utils.include_every_N_points_from(p_spiral_pins,2)


    # N = 5 # len(from_array_values)
    # for i in range(0,N):
    #     if i+1 in missing_screw_pins:
    #         sd.missing_screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i])
    #     else:
    #         sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i])
    #     #sd.move_pin_bool(from_array_values[i], vel, acc)

    N = 1
    for i in range(0,N):
        sd.screw_motion(vel, acc, home_pos, from_array_values[i], to_array_values[i], to_array_pins[i], from_array_pins[i])

    

    sd.move_home_bool(home_pos, vel, acc)
    sd.stop()

    screw_test_program = "/programs/screw_driver/Screw_test.urp"
    sd.robot.load_program(screw_test_program)


if __name__ == "__main__":
    try:
        csv_filename = "object_in_thread_test.csv"
        #run(csv_filename)

        #print(utils.include_every_N_points_from([2,3],2))

        to_anomalies = utils.include_every_N_points_from(a_spiral_pins,2)
        # print(to_anomalies)
        print(to_anomalies)

        #utils.join_plates(to_anomalies, a_seq_movement, a_spiral_pins, p_seq_pins, [c1])

        #all_pins = [i for i in range(1,92)]
        # t = utils.include_every_N_points_from(a_horizontal_pins,0)
        #u = utils.include_every_N_points_from(all_pins,2)
        # print(len(t))
        #print(u)

    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting program\n")
        sys.exit(0)
