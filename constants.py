import sys
import math

"""This file gathers constant values used for different robots such as the lengths of the leg parts, the angle conventions, initial positions, etc.
Also, to maintain compatibility with legacy code, the user can chose whether the input and/or outputs of the kinematic functions are in (rads or degs) and (mm or meters).
Values in this file should however always be written in meters and in rads.
"""

BIOLOID = "BIOLOID"
PHANTOMX = "PHANTOMX"
PHANTOMX_SIMULATION = "PHANTOMX_SIMULATION"
ARM_SIMULATION = "ARM_SIMULATION"
AX12 = "AX12"
MOTOR_TYPE = AX12
ROBOT_TYPE = PHANTOMX_SIMULATION
USING_SIMPLE_ROBOT = True
USE_RADS_INPUT = False
USE_RADS_OUTPUT = False
USE_MM_INPUT = False
USE_MM_OUTPUT = False

if ROBOT_TYPE == PHANTOMX:
    constL1 = 0.001 * 54.8
    constL2 = 0.001 * 65.3
    constL3 = 0.001 * 133
    theta2Correction = 16.0 * math.pi / 180.0
    theta2ExtraCorrection = 0
    theta3Correction = 43.76 * math.pi / 180.0  # -theta2Correction ??
    THETA3_MOTOR_SIGN = 1
    THETA2_MOTOR_SIGN = -1
    THETA1_MOTOR_SIGN = 1
    USE_RADS_INPUT = False
    USE_RADS_OUTPUT = False
    USE_MM_INPUT = False
    USE_MM_OUTPUT = False
    Z_DIRECTION = -1
    LEG_ANGLES = [
        -math.pi / 4,
        math.pi / 4,
        math.pi / 2,
        3 * math.pi / 4,
        -3 * math.pi / 4,
        -math.pi / 2,
    ]
elif ROBOT_TYPE == BIOLOID:
    constL1 = 0.001 * 51
    constL2 = 0.001 * 63.7
    constL3 = 0.001 * 93
    # Angle to match the theory with reality for theta 2 (measures of the triangle are 22.5, 60.7, 63.7). => Angle =  -20.69
    theta2Correction = -20.69 * math.pi / 180.0
    # Same goes for theta 3 : +90 - 20.69 - a. Where a = asin(8.2/93) = 5.06
    theta3Correction = (90 + theta2Correction - 5.06) * math.pi / 180.0
    THETA3_MOTOR_SIGN = -1
    THETA2_MOTOR_SIGN = 1
    THETA1_MOTOR_SIGN = 1
    USE_RADS_INPUT = False
    USE_RADS_OUTPUT = False
    USE_MM_INPUT = True
    USE_MM_OUTPUT = True
    Z_DIRECTION = -1
    LEG_ANGLES = [math.pi / 2, 0, 0, -math.pi / 2, math.pi, math.pi]
elif ROBOT_TYPE == PHANTOMX_SIMULATION:
    constL1 = 0.054
    constL2 = 0.0645
    constL3 = 0.155  # Approximate value (different from real robot and couldn't find value in URDF yet)
    theta2Correction = -16.0 * math.pi / 180.0  # Measured on real robot
    theta3Correction = (
        -43.76 * math.pi / 180.0 + theta2Correction
    )  # Measured on real robot
    THETA3_MOTOR_SIGN = -1
    THETA2_MOTOR_SIGN = 1
    THETA1_MOTOR_SIGN = 1
    USE_RADS_INPUT = True
    USE_RADS_OUTPUT = True
    USE_MM_INPUT = False
    USE_MM_OUTPUT = False
    Z_DIRECTION = 1
    LEG_ANGLES = [
        -math.pi / 4,
        math.pi / 4,
        math.pi / 2,
        3 * math.pi / 4,
        -3 * math.pi / 4,
        -math.pi / 2,
    ]
    LEG_CENTER_POS = [
        (0.1248, -0.06164, 0.001116),
        (0.1248, 0.06164, 0.001116),
        (0, 0.1034, 0.001116),
        (-0.1248, 0.06164, 0.001116),
        (-0.1248, -0.06164, 0.001116),
        (0, -0.1034, 0.001116),
    ]

elif ROBOT_TYPE == ARM_SIMULATION:
    constL1 = 0.085
    constL2 = 0.185
    constL3 = 0.250
    theta2Correction = 0
    theta3Correction = 0
    THETA3_MOTOR_SIGN = 1
    THETA2_MOTOR_SIGN = 1
    THETA1_MOTOR_SIGN = 1
    USE_RADS_INPUT = True
    USE_RADS_OUTPUT = True
    USE_MM_INPUT = False
    USE_MM_OUTPUT = False
    Z_DIRECTION = 1
else:
    print("ERROR: Unknwon ROBOT_TYPE '{}'".format(ROBOT_TYPE))
    sys.exit()
