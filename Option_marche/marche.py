from utils import SimpleRobotSimulation
from onshape_to_robot.simulation import Simulation
import kinematics
import time
import math
from scipy.spatial.transform import Rotation
import pybullet as p
from controle import Controle

class Marche:
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
        while True:
            keys = p.getKeyboardEvents()

            mode_rotation, mode_deplacement, extra_angle, is_idle = Controle.handle_keys(keys)

            self.robot.tick_read_and_write()
            val = 10 * math.sin(time.time()) * math.pi / 180

            index_patte1 = [1, 3, 5]
            index_patte2 = [2, 4, 6]

            for l in index_patte1:
                thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t, leg_id=l, extra_angle=extra_angle)
                for m in range(3):
                    self.robot.legs[l][m].goal_position = thetas[m]

            for l in index_patte2:
                thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t + 1, leg_id=l, extra_angle=extra_angle)
                for m in range(3):
                    self.robot.legs[l][m].goal_position = thetas[m]

            self.sim.tick()
