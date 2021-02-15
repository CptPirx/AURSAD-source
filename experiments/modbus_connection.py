"""
Establish Modbus TCP connection with the screwdriver.

Screwdriver address -> 65 (0x41)
Available function codes:
    - (0x03) Read holding registers
    - (0x06) Write Single Register
    - (0x10) Write Multiple Registers
    - (0x17) Read/Write Multiple Registers

To read a result print(results.registers)

"""

import sys
import time
import csv
import time
import numpy as np

from pymodbus.client.sync import ModbusTcpClient

unit = 0x41


def read_register(client, address, count, frequency, period):
    """
    Read a register for a specific period of time

    :param client: modbus client
    :param address: hex
        register address
    :param frequency: int
        the sampling frequency in Hz
    :param period: int
        read period in ms
    :return: list of readings
    """
    results_list = []
    loop_list = []

    read_start = time.time()
    for i in range(period):
        loop_start = time.time()
        result = client.read_holding_registers(address=address, count=count, unit=unit)
        results_list.append(result)
        time.sleep(1 / frequency)
        loop_end = time.time()
        loop_duration = loop_end - loop_start
        loop_list.append(loop_duration)

    read_end = time.time()
    read_time = read_end - read_start

    print(f'Average loop execution time: {np.mean(loop_list)}')
    print(f'Read duration time: {read_time}')

    return results_list


def save_registers(results_list):
    """
    Save the register values to csv file

    :param results_list: list of register objects
    :return:
    """
    list_lists = []

    for item in results_list:
        list_lists.append(item.registers)

    results_array = np.asarray(list_lists)

    np.savetxt('../test_results/Check_values.csv', results_array, delimiter=',')


def run():
    client = ModbusTcpClient(host='192.168.1.1', port=502)
    client.connect()
    print(client.is_socket_open())

    # time.sleep(1)
    # Screw length
    # client.write_register(address=0x0002, value=20000, unit=unit)
    # time.sleep(0.01)
    # # Z force
    # client.write_register(address=0x0001, value=18, unit=unit)
    # time.sleep(0.01)
    # # Target torque
    # client.write_register(address=0x0003, value=1000, unit=unit)
    # time.sleep(0.01)
    # # Command
    # client.write_register(address=0x0004, value=1, unit=unit)
    # Read given register for a period of time
    results_list = read_register(client=client, address=0x0100, count=6, period=5000, frequency=100)
    # time.sleep(2)

    # client.write_register(address=0x0004, value=4, unit=unit)

    save_registers(results_list=results_list)

    client.close()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting program\n")
        sys.exit(0)
