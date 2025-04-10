from XRPLib.defaults import *
from huskylensPythonLibrary import HuskyLensLibrary
import math
import time

# Initialize HuskyLens on I2C and differential drive system
husky = HuskyLensLibrary("I2C")
differentialDrive = DifferentialDrive.get_default_differential_drive()

# Ensure HuskyLens is in line tracking mode
while not husky.object_tracking_mode():
    husky.object_tracking_mode()

base_velocity = 15
# delta_velocity = 2

# Main loop
while True:
    state = husky.command_request_blocks()

    if len(state) > 0:
        state_vector = state[0]

        # x1 and x2 are the left and right points of the arrow
        state_x0 = state_vector[0] 
        state_x1 = state_vector[1]
        state_x2 = state_vector[2]  
        state_x3 = state_vector[3]

        # You could take either x1 or x2 as the X coordinate to track
        # x = (state_x0 + state_x1)/2  # center position box
        x = state_x0
        y = (state_x2 + state_x3)/2

        # Simple bang-bang controller
        if y < 55: 
            base_velocity = max(2* math.sqrt(57 - y),15)
            print(f"base velocity: {7* math.sqrt(57 - y),10}")
            if 150 <= x <= 170:
                # Go straight
                print("turn straight")
                differentialDrive.set_speed(base_velocity, base_velocity)  # both motors at 60% speed

            elif x < 150:
                # Turn left
                print("turn left")
                delta_velocity = (160-x)/10
                differentialDrive.set_speed(base_velocity-delta_velocity, base_velocity+delta_velocity)  # left motor slower

            elif x > 170:
                # Turn right
                print("turn right")
                delta_velocity = (x - 160)/10
                differentialDrive.set_speed(base_velocity+delta_velocity, base_velocity-delta_velocity)  # right motor slower
        if 55 <= y <= 62:
            differentialDrive.set_speed(0.0, 0.0)
        if y > 62:
            print("back up?")
            differentialDrive.set_speed(-12.0, -12.0)

        print(f"x0: {state_x0} \tx1: {state_x1} \tx2: {state_x2} \tx3: {state_x3}")

    else:
        # If no line detected, stop
        differentialDrive.set_speed(0.0, 0.0)

    time.sleep(0.1)