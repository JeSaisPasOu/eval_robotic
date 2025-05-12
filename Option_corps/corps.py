import kinematics
from utils import SimpleRobotSimulation
from onshape_to_robot.simulation import Simulation
import pybullet as p

class Corps:
    def __init__(self):
        self.robotPath = "phantomx_description/urdf/phantomx.urdf"
        self.sim = Simulation(self.robotPath, gui=True, panels=True, useUrdfInertia=False)
        self.sim.setRobotPose([0, 0, 0.5], p.getQuaternionFromEuler([0, 0, 0]))
        self.robot = SimpleRobotSimulation(self.sim)
        self.robot.init()
        print(self.robot)

    def run(self):
        x_value = float(input("Ecris la valeur de x :"))
        y_value = float(input("Ecris la valeur de y :"))
        z_value = float(input("Ecris la valeur de z :"))
        print("Voilà les coordonnées :", x_value, y_value, z_value)

        while True :
            for l in range(1,7):
                thetas = kinematics.computeIKOriented(x_value, y_value, z_value, None, 0)

                for m in range(0,3):
                    self.robot.legs[l][m].goal_position = thetas[m]

                self.sim.tick()
                self.robot.tick_read()

                if round(self.robot.legs[l][0].present_position, 4) == round(thetas[0],4) and round(self.robot.legs[l][1].present_position, 4) == round(thetas[1], 4) and round(self.robot.legs[l][2].present_position, 4) == round(thetas[2], 4):
                    break
