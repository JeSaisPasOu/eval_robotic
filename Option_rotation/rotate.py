from utils import SimpleRobotSimulation
from onshape_to_robot.simulation import Simulation
import kinematics
import time
import math
import pybullet as p
from scipy.spatial.transform import Rotation

class Rotate:
    def __init__(self):
        self.robotPath = "phantomx_description/urdf/phantomx.urdf"
        self.sim = Simulation(self.robotPath, gui=True, panels=True, useUrdfInertia=False)
        self.sim.setRobotPose([0, 0, 0.5], self.to_pybullet_quaternion(0, 0, 0, degrees=True))
        self.robot = SimpleRobotSimulation(self.sim)
        self.robot.init()
        print(self.robot)

    def to_pybullet_quaternion(self, roll, pitch, yaw, degrees=False):
        rot = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=degrees)
        return rot.as_quat()

    def run(self):
        mode_rotation = 0  # 0: normal, -1: gauche, +1: droite
        while True:
            self.robot.tick_read_and_write()

            keys = p.getKeyboardEvents()
            if ord('j') in keys and keys[ord('j')] & p.KEY_IS_DOWN:
                mode_rotation = -1
                print("Tourne à gauche")
            elif ord('l') in keys and keys[ord('l')] & p.KEY_IS_DOWN:
                mode_rotation = 1
                print("Tourne à droite")
            else:
                mode_rotation = 0

            # Groupes de jambes
            index_patte1 = [1, 3, 5]  # phase 0
            index_patte2 = [2, 4, 6]  # phase 1

            if mode_rotation == 0:
                # déplacement normal
                for l in index_patte1:
                    thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t, leg_id=l)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]

                for l in index_patte2:
                    thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t + 1, leg_id=l)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]
            else:
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

            self.sim.tick()
