"""
Various utility methods.
"""
from pathlib import Path
import os
import sys
import time
from datetime import datetime
from datetime import date
from screwdriver_utils import screwdriver
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from random import seed
from random import randint


def include_every_N_points_from(movement_seq, include_every_Nth, starting_point):
    movement_seq = movement_seq[starting_point:]
    if include_every_Nth == 0 or include_every_Nth == 1:
        print("Including all the points in the movement")
        return movement_seq
    else:
        return movement_seq[starting_point::include_every_Nth]


def save_points(points_from, points_to):
    filename = "prev_points.txt"
    with open(filename, 'a+') as f:
        f.write(f"{points_from},{points_to}\n")


def load_saved_points():
    filename = "prev_points.txt"
    if os.path.exists(filename):
        points_from = [int(x.split(',')[0]) for x in open(filename).readlines()]
        points_to = [int(x.split(',')[1]) for x in open(filename).readlines()]
    else:
        points_from, points_to = None, None
    return points_from, points_to


def join_plates(to_anomalies, original_from_plate, original_from_pins, to_pins, exchange_points):
    anomalies_index_to = []
    anomalies_pins_from = []

    # Check the index of the anomaly points in the to_sequence
    for anomaly_point in to_anomalies:
        anomalies_index_to.append(to_pins.index(anomaly_point))

    # Check the name of the point in the from sequence with index matching this of the to sequence
    for anomaly_index_to in anomalies_index_to:
        anomalies_pins_from.append(original_from_pins[anomaly_index_to])

    # Replace appropriate points in from sequence with the exchange sequence points
    exchange_i = 0
    exchanged_from_pins = original_from_pins
    for i in range(len(anomalies_pins_from)):
        if exchange_i >= len(exchange_points):
            exchange_i = 0
        original_from_plate[original_from_pins.index(anomalies_pins_from[i])] = exchange_points[exchange_i]
        exchanged_from_pins[anomalies_index_to[i]] = 93 + exchange_i
        exchange_i += 1

    return original_from_plate, exchanged_from_pins


def get_save_filename(folder, from_plate, to_plate):
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    date_format = str(today) + "_" + str(current_time)
    # get the first number of the folders inside the class results folder
    greatest = 0

    if not os.path.exists(folder):
        os.makedirs(folder)
    result_files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    for f in result_files:
        split_string = f.split('_')
        number = int(split_string[0])
        if number > greatest:
            greatest = number
    filename = str(greatest + 1) + "_" + str(from_plate) + "_to_" + str(to_plate) + "_" + date_format + ".csv"
    return filename


def load_screw_test_program(sd):
    screw_test_program = "/programs/screw_driver/Screw_test.urp"
    sd.robot.load_program(screw_test_program)


def setup_and_get_sd(folder, filename):
    sd = screwdriver.Screwdriver()
    sd.set_filename_and_config(save_exp_dir=folder,
                               config_file_dir=Path("resources"),
                               save_exp_filename=filename,
                               config_filename="record_configuration.xml")
    return sd


def create_random_anomalies(to_array_pins, n_anomalies, seed_source=time.time()):
    """
    Create a list of random anomalies points

    :param n_anomalies: int, number of anomalies to generate
    :param to_array_pins: list of ints, list of to_plate pins
    :return: list of ints, the anomaly points in the to_array
    """
    anomalies_list = []

    # seed random number generator
    seed(seed_source)
    # generate some integers
    for _ in range(n_anomalies):
        value = randint(1, max(to_array_pins) + 1)
        # Check if the generated value is in the list of pins
        while value not in to_array_pins:
            value = randint(1, max(to_array_pins) + 1)
        # Check if the value does not repeat itself
        while value in anomalies_list:
            value = randint(1, max(to_array_pins) + 1)
        anomalies_list.append(value)

    anomalies_list.sort()
    return anomalies_list


def save_data_with_anomalies(dir_name, file_name, to_anomalies, anomaly_label, from_pins, to_pins,
                             label_loosen=True):
    """
    Read the saved csv file with experiment results and add to it anomaly labels.

    :param: dir_name: Path directory
    :param: file_name: string, name of the file
    :param: to_anomalies: list of ints, list of to_points that are anomalies
    :param: anomaly_label: string, the label to assign to anomaly
    :param: from_pins: list of ints, sequence of points on from_plate
    :param: to_pins: list of ints, sequence of points on to_plate
    :param: label_loosen: bool, whether to label the loosening motion as part of the anomaly
    :return: the appended dataframe
    """
    dir_filename = dir_name / Path(file_name)
    data = pd.read_csv(filepath_or_buffer=dir_filename,
                       sep=' ')

    data['label'] = 0
    anomalies_index = []

    if label_loosen:
        # Check the index of the anomaly points in the to_sequence
        for anomaly_point in to_anomalies:
            anomalies_index.append(to_pins.index(anomaly_point))

        # Get to_points at these indices
        from_anomalies = [to_pins[i] for i in anomalies_index]

        # Label these points as anomalies
        data.loc[data['output_int_register_25'].isin(to_anomalies), "label"] = anomaly_label
        data.loc[data['output_int_register_26'].isin(from_anomalies), "label"] = anomaly_label
    else:
        data.loc[data['output_int_register_25'].isin(to_anomalies), "label"] = anomaly_label

    # Overwrite the file with new data
    data.to_csv(dir_filename, index=False, sep=" ")


if __name__ == "__main__":
    to_pins = [4, 5, 6, 7, 8]
    n_anomalies = 3

    create_random_anomalies(to_array_pins=to_pins,
                            n_anomalies=n_anomalies)
