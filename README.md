
# Relevant links
## Outputs from UR robot using urinterface

The link describes all the outputs and inputs to the robot.

https://www.universal-robots.com/articles/ur/real-time-data-exchange-rtde-guide/

## URScript Programming Language

https://s3-eu-west-1.amazonaws.com/ur-support-site/53318/scriptManual.pdf

# Set up instructions for using urinterface with URSIM
## Download URsim 

The link is for non-linux platforms, but can be changed for linux platforms if required.

https://www.universal-robots.com/download/?option=77063#section41570


## Setup VM network adapter

Follow the last section of the link (Part 8: Set Up of Network Adapter)

https://academy.universal-robots.com/media/jiehhszc/ursim_vmoracle_installation_guidev03_en.pdf


If you cannot ping from the VM to the host machine, then try checking out the following link:
https://superuser.com/questions/1214547/unable-to-ping-from-vms-to-host-machine


## Setup urinterface

Follow the instructions in the link:
https://pypi.org/project/urinterface/


## Run urinterface with URsim

Start the virtual machine, and start the program _URSim UR5_. Clikc on the _Power off_ button in the left corner. A new screen will be shown, with an _On_ button in the middle. Click the _On_ button, then clikc the _Start_ button. The virtual robot should now be on. The status of the robot is shown in the left bottom corner, where the status should now be _Normal_.
Run the file _run_experiment.py_ in the folder _robot_sim_tests_ and remember to specify the correct IP address of the virtual machine.

### Check if everything is working correctly

#### 1 Confirm the robot runs when you run the experiment

You can confirm if the robot starts running, when you run the python experiment by looking at the bottom left corner of the simulator. The figure below shows how the simulator looks when it is running.

<img src="assets/sim_running.png"
     alt="The robot is currently being simulated and is running"/>



#### 2 Change the specified IP address of the VM

You can also change the specified IP address of the VM and it should give an error, explaining it cannot make a connection.