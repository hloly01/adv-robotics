# Hannah Loly - ME 134 Advanced Robotics
# Lab 3 - Forward Kinematics
# python script to move robot and print data. 

from XRPLib.board import Board
from XRPLib.differential_drive import DifferentialDrive
from XRPLib.motor import Motor
from XRPLib.encoder import Encoder
from XRPLib.encoded_motor import EncodedMotor
from XRPLib.rangefinder import Rangefinder
from XRPLib.imu import IMU
from XRPLib.reflectance import Reflectance
from XRPLib.servo import Servo
from XRPLib.webserver import Webserver
from XRPLib.timeout import *
import time
import math
import random

# get defaults
print("start")
left_motor = EncodedMotor.get_default_encoded_motor(index=1)
right_motor = EncodedMotor.get_default_encoded_motor(index=2)
imu = IMU.get_default_imu()
drivetrain = DifferentialDrive.get_default_differential_drive()
rangefinder = Rangefinder.get_default_rangefinder()
reflectance = Reflectance.get_default_reflectance()
servo_one = Servo.get_default_servo(index=1)
servo_two = Servo.get_default_servo(index=2)
webserver = Webserver.get_default_webserver()
board = Board.get_default_board()

'''first go straight and turn right '''

# create a new file (or overwrite an existing one) to add data to
raw = open("raw_data.csv", "w")
calculated = open("IK_Kalman.csv", "w")
# reset encoder positions
left_motor.reset_encoder_position()
right_motor.reset_encoder_position()

class Kalman: 
    def __init__(self):
        self.cmpsToRPM = 60 / (math.pi * 6) # see differential_drive.py
        self.RPMTocmps = 1/self.cmpsToRPM
        self.track_width = 16 # [cm]
        self.dt = .1
        self.theta_calc = 0
        # state estimates
        self.x = self.y = self.theta = 0.0      # X(k,k)    - state of robot
        self.x_x = self.x_y = self.x_theta = 0  # X(K, k-1) - intermediate result from model
        self.z_x = self.z_y = self.z_theta = 0  # z         - additional sensor measurement
        # covariance matrices
        self.P = [
            [.1, 0, 0],
            [0, .1, 0],
            [0, 0, .1]
        ]
        # prediction noise
        self.Q = [
            [.1, 0, 0],
            [0, .1, 0],
            [0, 0, .1]
        ]
        # measurement noise
        self.R = [
            [.05, 0, 0],
            [0, .05, 0],
            [0, 0, .5]  
        ]

    def matrix_addition(self, A, B):
            return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    def matrix_multiply(self, A, B):
            return[
                [sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
                for i in range(len(A))
            ]
    def update_step(self):
         
        # kalman update for theta
        gyro_z_rad_per_s = imu.get_gyro_z_rate() * (math.pi/180000)
        self.z_theta += gyro_z_rad_per_s * self.dt

        innovation = self.z_theta - self.x_theta
        P_theta = self.P[2][2]
        R_theta = self.R[2][2]
        K_theta = P_theta/(P_theta + R_theta)
        self.theta = self.x_theta + K_theta * innovation
        self.x_theta = self.theta
        self.P[2][2] = (1-K_theta) * self.P[2][2]
        calculated.write(f"{self.x} {self.y} {self.theta}\n")
         
    def prediction_step(self):
        left_speed = left_motor.get_speed() * self.RPMTocmps
        right_speed = right_motor.get_speed() * self.RPMTocmps
        w = (right_speed - left_speed) / self.track_width
        # Kinematic model estimate using x_theta
        if w == 0:
            V = 0.5 * (left_speed + right_speed)
            self.x_x += V * math.cos(self.x_theta) * self.dt
            self.x_y += V * math.sin(self.x_theta) * self.dt
        else:
            R_val = self.track_width * (right_speed + left_speed) / (2 * (right_speed - left_speed))
            self.x_x += -R_val * math.sin(self.x_theta) + R_val * math.sin(self.x_theta + w * self.dt)
            self.x_y += R_val * math.cos(self.x_theta) - R_val * math.cos(self.x_theta + w * self.dt)
            self.x_theta += w * self.dt
        self.P = self.matrix_addition(self.P, self.Q)
        # Kalman update for theta
        self.update_step()

def drive():
    while timer.is_done() != 1:
        # read encoder values and heading every .1 sec for 10 sec
        pos_left = left_motor.get_position_counts()
        pos_right = right_motor.get_position_counts()
        imu_omega = imu.get_acc_z()
        pos_avg = (pos_left+pos_right)/2 # distance center of robot has traveled 
        heading = imu.get_heading()
        kalman.prediction_step()
        raw.write(f"{pos_left} {pos_right} {heading} {imu_omega}\n")
        time.sleep(kalman.dt)
    drivetrain.set_speed(0,0)


kalman = Kalman()
# set hardware timer
print("start timer ")
timer = Timeout(5) # start timer for 30 sec

print("start moving")
drivetrain.set_speed(25, 25) # set speed for circle (use 20,20 for straight and 15,20 for curve)
drive()

''' code to spin '''
timer = Timeout(12)
print("start spinning")
drivetrain.set_speed(-30, 30)
drive()

'''another drive section'''
print("go straight")
timer = Timeout(5)
drivetrain.set_speed(25,25)
drive()

raw.close()
calculated.close()


