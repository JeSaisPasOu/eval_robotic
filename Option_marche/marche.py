import utils
from utils import SimpleRobotSimulation
from onshape_to_robot.simulation import Simulation
import kinematics
import time
import math

from scipy.spatial.transform import Rotation

def testIKOriented(sim, robot):
    val= 0.05* math.sin(sim.t)
    for i in range(6):
        leg= robot.legs[i+1]
        thetas= kinematics.computeIKOriented(val, 0, 0, i+1)
        for m in range(0,3):
            leg[m].goal_position = thetas[m]

def to_pybullet_quaternion(roll, pitch, yaw, degrees=False):
    # Create a rotation object from Euler angles specifying axes of rotation
    rot = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=degrees)
    rot_quat = rot.as_quat()

    return rot_quat

robotPath = "phantomx_description/urdf/phantomx.urdf"
sim = Simulation(robotPath, gui=True, panels=True, useUrdfInertia=False)
pos, rpy = sim.getRobotPose()
sim.setRobotPose([0, 0, 0.5], to_pybullet_quaternion(0, 0, 0, degrees=True))
robot = SimpleRobotSimulation(sim)
robot.init()
print(robot)


robot.legs[1][0].goal_position= math.pi/2
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

while True:
    robot.tick_read_and_write()

    val=10*math.sin(time.time())*math.pi/180

    index_patte1 = [1,3,5]
    index_patte2 = [2,4,6]

    for l in index_patte1:
        thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, sim.t, leg_id=l)
        for m in range(0,3):
            robot.legs[l][m].goal_position = thetas[m]

    for l in index_patte2:
        thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, sim.t+1, leg_id= l)
        for m in range(0,3):
            robot.legs[l][m].goal_position = thetas[m]

    
    sim.tick()

