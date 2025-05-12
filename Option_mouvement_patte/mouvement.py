import kinematics
from utils import SimpleRobotSimulation
from onshape_to_robot.simulation import Simulation
import pybullet as p

class Mouvement :
        def __init__(self):
            self.robotPath = "phantomx_description/urdf/phantomx.urdf"
            self.sim = Simulation(self.robotPath, gui=True, panels=True, useUrdfInertia=False)
            self.sim.setRobotPose([0, 0, 0.5], p.getQuaternionFromEuler([0, 0, 0]))
            self.robot = SimpleRobotSimulation(self.sim)
            self.robot.init()
            print(self.robot)

        def run(self):
            patte = int(input("Ecris le numéro de la patte :"))
            x_value = float(input("Ecris la valeur de x :"))
            y_value = float(input("Ecris la valeur de y :"))
            z_value = float(input("Ecris la valeur de z :"))
            print("Voilà les valeurs : ", patte, x_value, y_value, z_value)

            thetas = kinematics.computeIK(x_value, y_value, z_value)

            print("Appuie sur 'Q' pour quitter la simulation")

            while True:
                keys = p.getKeyboardEvents()
                if ord('q') in keys and keys[ord('q')] & p.KEY_WAS_TRIGGERED:
                    print("Fermeture de la simulation demandée.")
                    break

                for m in range(3):
                    self.robot.legs[patte][m].goal_position = thetas[m]

                self.sim.tick()
                self.robot.tick_read()

                if all(
                    round(self.robot.legs[patte][i].present_position, 4) == round(thetas[i], 4)
                    for i in range(3)
                ):
                    pass  # tu peux ajouter une pause ou animation ici

            p.disconnect()
