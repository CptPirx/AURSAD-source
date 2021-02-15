import matplotlib.pyplot as plt
import third_party.rtde.csv_reader as csv_reader
from pathlib import Path

f_name = "pick_place_motion_ur5.csv"
filename = Path("test_results") / Path(f_name)
print(f"filename: {filename}")
with open(filename) as csvfile:
    rd = csv_reader.CSVReader(csvfile) # robot data object

t = rd.timestamp - rd.timestamp[0]
q_0 = rd.target_q_0
q_1 = rd.target_q_1
q_2 = rd.target_q_2
plt.plot(t, q_0, label='q_0')
plt.plot(t, q_1, label='q_1')
plt.plot(t, q_2, label='q_2')
plt.xlabel('Time [s]')
plt.ylabel('Target Angular Position [rad]')
plt.legend()
plt.show()

