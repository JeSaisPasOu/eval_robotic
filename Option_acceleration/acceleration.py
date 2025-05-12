from utils import SimpleRobotSimulation, Parameters
from onshape_to_robot.simulation import Simulation
import kinematics
import utils

import time
import math
import pybullet as p
from scipy.spatial.transform import Rotation
from controle import Controle


class Acceleration:
    def __init__(self):
        self.robotPath = "phantomx_description/urdf/phantomx.urdf"
        self.sim = Simulation(self.robotPath, gui=True, panels=True, useUrdfInertia=False)
        self.sim.setRobotPose([0, 0, 0.5], self.to_pybullet_quaternion(0, 0, 0, degrees=True))
        self.robot = SimpleRobotSimulation(self.sim)
        self.robot.init()
        print(self.robot)

        # Ajout des curseurs pour ajuster les paramètres de marche
        self.slider_speed = p.addUserDebugParameter("vitesse_deplacement", 0.1, 5.0, 1.0)
        self.slider_amplitude = p.addUserDebugParameter("Amplitude", 0.01, 0.1, 0.08)
        self.slider_height = p.addUserDebugParameter("Hauteur", 0.01, 0.1, 0.05)
        self.slider_frequency = p.addUserDebugParameter("Frequence", 0.1, 16.0, 1.0)

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

        # Récupération des paramètres dynamiques via les curseurs
        extra_angle = 0

        mode_rotation = 0  # 0: normal, -1: gauche, +1: droite
        mode_deplacement = False
        index_patte = [1, 2, 3, 4, 5, 6]
        is_idle = True  # Robot au repos au départ

        utils.setPositionToRobot(0, 0, 0.05, self.robot, self.params, extra_theta=0)
        self.robot.smooth_tick_read_and_write(1, verbose=True)
        while True:
            speed = p.readUserDebugParameter(self.slider_speed)
            amplitude = p.readUserDebugParameter(self.slider_amplitude)
            height = p.readUserDebugParameter(self.slider_height)
            frequency = p.readUserDebugParameter(self.slider_frequency)

            keys = p.getKeyboardEvents()

            mode_rotation, mode_deplacement, extra_angle, is_idle = Controle.handle_keys(keys)


            # Groupes de jambes
            index_patte1 = [1, 3, 5]  # phase 0
            index_patte2 = [2, 4, 6]  # phase 1

            # Calcul de la position des jambes selon les paramètres dynamiques
            if mode_deplacement:
                for l in index_patte1:
                    thetas = kinematics.triangle(0, -0.05, height, amplitude, self.sim.t * frequency, leg_id=l, extra_angle=extra_angle)

                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]

                for l in index_patte2:
                    thetas = kinematics.triangle(0, -0.05, height, amplitude, (self.sim.t + 1) * frequency , leg_id=l, extra_angle=extra_angle)
                    print(height)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]

            elif mode_rotation != 0:
                # Rotation
                t_inverse = self.sim.t * mode_rotation

                for l in index_patte1:
                    thetas = kinematics.triangle(0.2, -0.10, height, amplitude, t_inverse)
                    for m in range(0, 3):
                        self.robot.legs[l][m].goal_position = thetas[m]

                for l in index_patte2:
                    thetas = kinematics.triangle(0.2, -0.10, height, amplitude, t_inverse + 1)
                    for m in range(0, 3):
                        self.robot.legs[l][m].goal_position = thetas[m]

            else:
                # Repos
                utils.setPositionToRobot(0, 0, 0.05, self.robot, self.params, extra_theta=0)
                        

            # self.robot.smooth_tick_read_and_write(0.01, verbose=True)
            self.robot.tick_read_and_write()

            self.sim.tick()
