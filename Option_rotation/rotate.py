from utils import SimpleRobotSimulation, Parameters
from onshape_to_robot.simulation import Simulation
import kinematics
import utils

import time
import math
import pybullet as p
from scipy.spatial.transform import Rotation
from controle import Controle

class Rotate:
    def __init__(self):
        self.robotPath = "phantomx_description/urdf/phantomx.urdf"
        self.sim = Simulation(self.robotPath, gui=True, panels=True, useUrdfInertia=False)
        self.sim.setRobotPose([0, 0, 0.5], self.to_pybullet_quaternion(0, 0, 0, degrees=True))
        self.robot = SimpleRobotSimulation(self.sim)
        self.robot.init()
        print(self.robot)
        self.params = Parameters(
            freq=50,
            speed=1,
            z=80,
            travelDistancePerStep=80,
            lateralDistance=110,
            frontDistance=87,
            frontStart=32,
            method="minJerk",
        )

    def to_pybullet_quaternion(self, roll, pitch, yaw, degrees=False):
        rot = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=degrees)
        return rot.as_quat()

    def run(self):
        mode_rotation = 0  # 0: normal, -1: gauche, +1: droite
        mode_deplacement = False
        index_patte = [1, 2, 3, 4, 5, 6]
        is_idle = True  # Robot au repos au départ

        utils.setPositionToRobot(0, 0, 0.05, self.robot, self.params, extra_theta=0)
        self.robot.smooth_tick_read_and_write(1, verbose=True)
        while True:

            keys = p.getKeyboardEvents()
            mode_rotation, mode_deplacement, extra_angle, is_idle = Controle.handle_keys(keys)

            # Groupes de jambes
            index_patte1 = [1, 3, 5]  # phase 0
            index_patte2 = [2, 4, 6]  # phase 1

            if mode_deplacement :
                # déplacement normal
                
                for l in index_patte1:
                    thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t, leg_id=l, extra_angle=extra_angle)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]

                for l in index_patte2:
                    thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t + 1, leg_id=l, extra_angle=extra_angle)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]
            elif mode_rotation != 0:
                # rotation : +x pour droite, -x pour gauche
                t_inverse = self.sim.t * mode_rotation

                for l in index_patte1:
                    thetas = kinematics.triangle(0.2, -0.10, 0.03, 0.08, t_inverse)
                    for m in range(0,3):
                        self.robot.legs[l][m].goal_position = thetas[m]

                for l in index_patte2:
                    thetas = kinematics.triangle(0.2, -0.10, 0.03, 0.08, t_inverse+1)
                    for m in range(0,3):
                        self.robot.legs[l][m].goal_position = thetas[m]

            else:
                # Repos
                utils.setPositionToRobot(0, 0, 0.05, self.robot, self.params, extra_theta=0)
                        

            # self.robot.smooth_tick_read_and_write(0.01, verbose=True)
            self.robot.tick_read_and_write()

            self.sim.tick()
