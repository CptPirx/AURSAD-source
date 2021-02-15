import os
import sys
import time
from pathlib import Path

import pandas as pd
from urinterface.robot_connection import RobotConnection


class Screwdriver:

    def __init__(self, ip="192.168.1.2",
                 register_move_pin=64,
                 register_move_home=65,
                 register_loosen=66,
                 register_tighten=67,
                 register_int_to_plate=25,
                 register_int_from_plate=26,
                 save_exp_dir=None,
                 config_file_dir=None,
                 save_exp_filename="test_results.csv",
                 config_filename="record_configuration.xml"):
        self.robot = RobotConnection(ip)
        self.register_move_home = register_move_home
        self.register_move_pin = register_move_pin
        self.register_loosen = register_loosen
        self.register_tighten = register_tighten
        self.register_int_to_plate = register_int_to_plate
        self.register_int_from_plate = register_int_from_plate
        self.set_filename_and_config(save_exp_dir, config_file_dir, save_exp_filename, config_filename)

    def set_filename_and_config(self, save_exp_dir=None, config_file_dir=None, save_exp_filename="test_results.csv",
                                config_filename="record_configuration.xml"):
        if save_exp_dir == None:
            self.filename = Path("test_results") / Path(save_exp_filename)
        else:
            self.filename = Path(save_exp_dir) / Path(save_exp_filename)
        if config_file_dir == None:
            self.config_file = Path("resources") / Path("record_configuration.xml")
        else:
            self.config_file = Path(config_file_dir) / Path(config_filename)

    def set_bool_output_peak(self, registerNo):
        self.robot._send_ctrl_cmd("write_output_boolean_register(" + str(registerNo) + ", True)\n")
        self.robot._send_ctrl_cmd("write_output_boolean_register(" + str(registerNo) + ", False)\n")

    def reset_outputs(self):
        self.robot._send_ctrl_cmd("write_output_boolean_register(" + str(self.register_move_home) + ", False)\n")
        self.robot._send_ctrl_cmd("write_output_boolean_register(" + str(self.register_move_pin) + ", False)\n")
        self.robot._send_ctrl_cmd("write_output_boolean_register(" + str(self.register_loosen) + ", False)\n")
        self.robot._send_ctrl_cmd("write_output_boolean_register(" + str(self.register_tighten) + ", False)\n")
        self.set_int_from_plate(0)
        self.set_int_to_plate(0)

    def pick_up_screw(self, previous_waypoint):
        pick_up_program_name = "/programs/screw_driver/pick_up.urp"
        self.robot.load_program(pick_up_program_name)
        self.robot.play_program()
        time.sleep(1)
        self.robot.movej(previous_waypoint, v=1.0, a=0.5)

    def loosen_screw(self, previous_waypoint):
        loosen_program_name = "/programs/screw_driver/loosen_thread.urp"
        self.robot.load_program(loosen_program_name)
        self.robot.play_program()
        time.sleep(1)
        self.robot.movej(previous_waypoint, v=1.0, a=0.5)

    def tighten_screw(self, previous_waypoint):
        tighten_program_name = "/programs/screw_driver/tighten_thread.urp"
        self.robot.load_program(tighten_program_name)
        self.robot.play_program()
        time.sleep(1)
        self.robot.movej(previous_waypoint, v=1.0, a=0.5)

    def idle_thread(self, previous_waypoint):
        program_name = "/programs/screw_driver/idle_thread.urp"
        self.set_bool_output_peak(self.register_loosen)  # Set peak on loosen screw register
        self.robot.load_program(program_name)
        self.robot.play_program()
        time.sleep(0.5)
        self.robot.stop_program()
        self.robot.movej(previous_waypoint, v=1.0, a=0.5)

    def set_int_from_plate(self, pin):
        self.robot._send_ctrl_cmd(
            "write_output_integer_register(" + str(self.register_int_from_plate) + ", " + str(pin) + ")\n")

    def set_int_to_plate(self, pin):
        self.robot._send_ctrl_cmd(
            "write_output_integer_register(" + str(self.register_int_to_plate) + ", " + str(pin) + ")\n")

    def move_pin_bool(self, position, v, a):
        self.set_bool_output_peak(self.register_move_pin)
        self.robot.movej(position, v=v, a=a)

    def move_home_bool(self, position, v, a):
        self.set_bool_output_peak(self.register_move_home)
        self.robot.movej(position, v=v, a=a)

    def screw_motion(self, v, a, home_pos, pos1, pos2, to_pin=0, from_pin=0):
        # Move to home then hole 1
        self.set_int_from_plate(from_pin)
        self.move_pin_bool(pos1, v=v, a=a)
        # Loosen screw
        self.loosen_screw(pos1)
        # Move to home then hole 2
        self.move_home_bool(home_pos, v=v, a=a)
        self.set_int_to_plate(to_pin)
        self.set_int_from_plate(0)
        self.move_pin_bool(pos2, v=v, a=a)
        # Tighten screw
        self.tighten_screw(pos2)
        self.move_home_bool(home_pos, v=v, a=a)
        self.set_int_to_plate(0)

    def missing_screw_motion(self, v, a, home_pos, pos1, pos2, to_pin=0, from_pin=0):
        # Move to home then hole 1
        self.set_int_from_plate(from_pin)
        self.move_pin_bool(pos1, v=v, a=a)
        # Immitate missing screw
        self.idle_thread(pos1)
        # Move to home then hole 2
        self.move_home_bool(home_pos, v=v, a=a)
        self.set_int_to_plate(to_pin)
        self.set_int_from_plate(0)
        self.move_pin_bool(pos2, v=v, a=a)
        # Tighten screw
        self.tighten_screw(pos2)
        self.move_home_bool(home_pos, v=v, a=a)
        self.set_int_to_plate(0)

    def damaged_screw_thread_motion(self, v, a, home_pos, pos1, pos2, to_pin=0, from_pin=0):
        # Move to home then hole 1
        self.set_int_from_plate(from_pin)
        self.move_pin_bool(pos1, v=v, a=a)
        time.sleep(0.1)
        # Pick up screw
        self.pick_up_screw(pos1)
        # Move to home then hole 2
        self.move_home_bool(home_pos, v=v, a=a)
        self.set_int_to_plate(to_pin)
        self.set_int_from_plate(0)
        self.move_pin_bool(pos2, v=v, a=a)
        # Tighten screw
        self.tighten_screw(pos2)
        self.move_home_bool(home_pos, v=v, a=a)
        self.set_int_to_plate(0)

    def start(self):
        self.reset_outputs()
        self.robot.start_recording(filename=self.filename, overwrite=True, config_file=self.config_file, frequency=100)

    def stop(self):
        self.robot.stop_recording()
        self.reset_outputs()
