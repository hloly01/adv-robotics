from XRPLib.defaults import *
from Husky.huskylensPythonLibrary import HuskyLensLibrary
import math
import time

try:
    from MQTT.mqttconnect import *
    use_mqtt = True
    print("MQTT library found, running with MQTT.")
except ImportError:
    use_mqtt = False
    print("MQTT library not found, running without MQTT.")

# Initialize HuskyLens on I2C and differential drive system
husky = HuskyLensLibrary("I2C")
differentialDrive = DifferentialDrive.get_default_differential_drive()
if use_mqtt:
    c = connect_mqtt()
    c.ping()

# Ensure HuskyLens is in line tracking mode
while not husky.color_recognition_mode():
    husky.color_recognition_mode()
base_velocity = 15
state_history = []
# delta_velocity = 2
# Main loop
repeat = 71
while not board.is_button_pressed():
    state = husky.command_request_blocks()
    if len(state) > 0:
        repeat = 1
        state_vector = state[0]
        state_x0 = state_vector[0] # x-coord
        state_x1 = state_vector[1]
        state_x2 = state_vector[2] # y-coord top
        state_x3 = state_vector[3] # y-coord bottom
        # You could take either x1 or x2 as the X coordinate to track
        # x = (state_x0 + state_x1)/2  # center position box
        x = state_x0
        y = (state_x2 + state_x3)/2
        # Bang-bang controller w/ proportional control
        if y < 68:
            base_velocity = max(10* math.sqrt(abs(68 - y)),15)
            P = .2
            print(f"base velocity: {10* math.sqrt(abs(68 - y)),15}")
            if 150 <= x <= 170:
                # Go straight
                print("drive straight")
                differentialDrive.set_speed(base_velocity, base_velocity)
            elif x < 150:
                # Turn left
                print("turn left")
                delta_velocity = P*(160-x)
                differentialDrive.set_speed(base_velocity-delta_velocity, base_velocity+delta_velocity)  # left motor slower
            elif x > 170:
                # Turn right
                print("turn right")
                delta_velocity = P*(x - 160)
                differentialDrive.set_speed(base_velocity+delta_velocity, base_velocity-delta_velocity)  # right motor slower
        elif 68 <= y <= 75:
            differentialDrive.set_speed(0.0, 0.0)
            base_velocity = 0
            delta_velocity = 0
        elif y > 75:
            print("back up")
            differentialDrive.set_speed(-12.0, -12.0)
            base_velocity = -12
            delta_velocity = 0
        print(f"x0: {state_x0} \tx1: {state_x1} \tx2: {state_x2} \tx3: {state_x3}")
        state_history.append([state_x0,state_x1,state_x2,state_x3])
        # state_history.append("/n")
        if use_mqtt:
            c.publish("topic/HONK_Results", str([state_x0,state_x1,state_x2,state_x3 ]), retain=True)
            if len(state_history) > 10:
                for i in range(1, 11):
                    c.publish(f"topic/HONK_Results_{i}", str(state_history[-i]), retain=True)
    else:
        # If no object detected, go straight at base velocity 3 times, then stop
        if repeat < 70:
            differentialDrive.set_speed(base_velocity, base_velocity)
            print(f"reapeat {repeat}")
            repeat+=1
            time.sleep(.1)
        differentialDrive.set_speed(0.0, 0.0)
    time.sleep(0.1)