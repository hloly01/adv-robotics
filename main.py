from XRPLib.defaults import *
from huskylensPythonLibrary import HuskyLensLibrary
import math
import time
from mqttconnect import *
from XRPLib.timeout import *

# Initialize HuskyLens on I2C and differential drive system
husky = HuskyLensLibrary("I2C")
differentialDrive = DifferentialDrive.get_default_differential_drive()
c = connect_mqtt()
if c == None: 
    MQTT = 0
    print("MQTT failed to connect")
else: 
    MQTT = 1
    c.ping()

# Ensure HuskyLens is in color recognition mode
while not husky.color_recognition_mode():
    husky.color_recognition_mode()

# STAGE 1: move forward for 5 seconds to demonstrate walking robots
def test_walk():
    print("walk!")
    timer = Timeout(5) # start timer for 30 sec
    drivetrain.set_speed(25, 25)
    while timer.is_done() != 1:
        time.sleep(.1) # spin loop
    print("done walking :)")
    drivetrain.set_speed(0,0)

# STAGE 2: track person using color tracking and proportional control. 
def follow_person():
    base_velocity = 15
    P = 0.2
    state_history = []
    repeat = 71
    previous_x = 200  # To detect wraparound
    while not board.is_button_pressed():
        state = husky.command_request_blocks()
        
        if len(state) > 0:
            repeat = 1
            state_vector = state[0]
            state_x0 = state_vector[0]  # x-coord
            state_x1 = state_vector[1]
            state_x2 = state_vector[2]  # y-coord top
            state_x3 = state_vector[3]  # y-coord bottom

            x = state_x0
            y = (state_x2 + state_x3) / 2
            update = 1

            # use position in screen to determine robot movement. y determines forward motion, x determines turning

            if y < 68: # object in top of screen, move forward 
                # choose a base velocity that reflects how far the person is
                base_velocity = -1*max(10 * math.sqrt(abs(68 - y)), 15)
                print(f"base velocity: {base_velocity:.2f}")

                # --- WRAPAROUND DETECTION ---
                if previous_x is not None and previous_x > 200 and x < 60:
                    print(f"wraparound detected → turn right({base_velocity+delta_velocity, base_velocity - delta_velocity})")
                    differentialDrive.set_speed(base_velocity + delta_velocity, base_velocity - delta_velocity)
                    # don't update previous state if there is a wraparound
                    update = 0 
                
                # --- NORMAL TRACKING ---
                elif 150 <= x <= 170:
                    print("drive straight")
                    differentialDrive.set_speed(base_velocity, base_velocity)

                elif x < 150:
                    print("turn left")
                    delta_velocity = P * (160 - x)
                    differentialDrive.set_speed(base_velocity - delta_velocity, base_velocity + delta_velocity)

                elif x > 170:
                    print("turn right")
                    delta_velocity = P * (x - 160)
                    differentialDrive.set_speed(base_velocity + delta_velocity, base_velocity - delta_velocity)

            # object in center of screen, wait to proceed
            elif 68 <= y <= 75:
                differentialDrive.set_speed(0.0, 0.0)
                base_velocity = 0
                delta_velocity = 0
            
            # object too close to robot, back up
            elif y > 75:
                print("back up")
                differentialDrive.set_speed(-12.0, -12.0)
                base_velocity = -12
                delta_velocity = 0

            print(f"x0: {state_x0} \tx1: {state_x1} \tx2: {state_x2} \tx3: {state_x3}")
            if MQTT: # If connected to MQTT, publish results 
                state_history.append([state_x0, state_x1, state_x2, state_x3])
                c.publish("topic/HONK_Results", str([state_x0, state_x1, state_x2, state_x3]), retain=True)

                if len(state_history) > 10:
                    for i in range(1, 11):
                        c.publish(f"topic/HONK_Results_{i}", str(state_history[-i]), retain=True)

            if update: 
                previous_x = x  # Save last x

        else:
            # move forward for 5 seconds in an attempt to relocate person. then stop
            if repeat < 50:
                differentialDrive.set_speed(base_velocity, base_velocity)
                print(f"repeat {repeat}")
                repeat += 1
                time.sleep(0.1)
            differentialDrive.set_speed(0.0, 0.0)
        time.sleep(0.1)

# run the code! 
test_walk()
follow_person()
