from utils import SimpleRobotSimulation, Parameters
from onshape_to_robot.simulation import Simulation
import kinematics
import utils

import time
import math
import pybullet as p
from scipy.spatial.transform import Rotation
from controle import Controle
import xml.etree.ElementTree as ET

class Marche_controle:
    def __init__(self):
        self.robotPath = "phantomx_description/urdf/phantomx.urdf"
        self.sim = Simulation(self.robotPath, gui=True, panels=True, useUrdfInertia=False)
        self.sim.setRobotPose([0, 0, 0.5], self.to_pybullet_quaternion(0, 0, 0, degrees=True))
        self.robot = SimpleRobotSimulation(self.sim)
        self.robot.init()
        print(self.robot)
        self.params = Parameters(
            freq=100,
            speed=3,
            z=80,
            travelDistancePerStep=80,
            lateralDistance=110,
            frontDistance=87,
            frontStart=32,
            method="minJerk",
        )
        self.recording = False
        self.recorded_frames = []
        self.coord_text_id = None


    def to_pybullet_quaternion(self, roll, pitch, yaw, degrees=False):
        rot = Rotation.from_euler("xyz", [roll, pitch, yaw], degrees=degrees)
        return rot.as_quat()

    def record_frame(self):
        frame = {}
        for leg_id, motors in self.robot.legs.items():
            frame[str(leg_id)] = [motor.goal_position for motor in motors]
        self.recorded_frames.append(frame)

    def export_to_xml(self, filename="record.xml"):
        root = ET.Element("sequence")
        for i, frame in enumerate(self.recorded_frames):
            frame_elem = ET.SubElement(root, "frame", id=str(i))
            for leg_id, angles in frame.items():
                joint_elem = ET.SubElement(frame_elem, "leg", id=leg_id)
                joint_elem.set("c1", str(angles[0]))
                joint_elem.set("c2", str(angles[1]))
                joint_elem.set("c3", str(angles[2]))
        tree = ET.ElementTree(root)
        tree.write(filename)
        print(f"💾 Mouvements enregistrés dans {filename}")

    def replay_reverse(self, filename="record.xml"):
        print("🔁 Relecture des mouvements à l’envers...")
        tree = ET.parse(filename)
        root = tree.getroot()
        frames = list(root.findall("frame"))
        for frame in reversed(frames):
            for leg_elem in frame.findall("leg"):
                leg_id = int(leg_elem.attrib["id"])
                c1 = float(leg_elem.attrib["c1"])
                c2 = float(leg_elem.attrib["c2"])
                c3 = float(leg_elem.attrib["c3"])
                self.robot.legs[leg_id][0].goal_position = c1
                self.robot.legs[leg_id][1].goal_position = c2
                self.robot.legs[leg_id][2].goal_position = c3
            self.robot.tick_read_and_write()
            self.sim.tick()
            time.sleep(1 / self.params.freq)
        print("✅ Relecture terminée.")

    def run(self):
        mode_rotation = 0
        mode_deplacement = False
        index_patte = [1, 2, 3, 4, 5, 6]
        is_idle = True

        utils.setPositionToRobot(0, 0, 0.05, self.robot, self.params, extra_theta=0)
        self.robot.smooth_tick_read_and_write(1, verbose=True)

        while True:
            keys = p.getKeyboardEvents()

            # ESC pour quitter proprement
            if 27 in keys and keys[27] & p.KEY_WAS_TRIGGERED:
                if self.recording:
                    self.export_to_xml()
                break

             # O pour rotation + relecture à l’envers
            if ord('o') in keys and keys[ord('o')] & p.KEY_WAS_TRIGGERED:
                self.replay_reverse("record.xml")

            # P pour démarrer/arrêter l'enregistrement
            if ord('p') in keys and keys[ord('p')] & p.KEY_WAS_TRIGGERED:
                self.recording = not self.recording
                if self.recording:
                    self.recorded_frames = []  # Réinitialiser les frames
                    print("🔴 Enregistrement démarré.")
                else:
                    print("🟢 Enregistrement arrêté.")
                    self.export_to_xml()

            mode_rotation, mode_deplacement, extra_angle, is_idle = Controle.handle_keys(keys)

            index_patte1 = [1, 3, 5]
            index_patte2 = [2, 4, 6]

            if mode_deplacement:
                for l in index_patte1:
                    thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t, leg_id=l, extra_angle=extra_angle)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]
                for l in index_patte2:
                    thetas = kinematics.triangle(0, -0.05, 0.03, 0.08, self.sim.t + 1, leg_id=l, extra_angle=extra_angle)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]
            elif mode_rotation != 0:
                t_inverse = self.sim.t * mode_rotation
                for l in index_patte1:
                    thetas = kinematics.triangle(0.2, -0.10, 0.03, 0.08, t_inverse)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]
                for l in index_patte2:
                    thetas = kinematics.triangle(0.2, -0.10, 0.03, 0.08, t_inverse + 1)
                    for m in range(3):
                        self.robot.legs[l][m].goal_position = thetas[m]
            else:
                utils.setPositionToRobot(0, 0, 0.05, self.robot, self.params, extra_theta=0)

            if self.recording:
                self.record_frame()

            # Récupérer la position du robot et afficher dans la simulation 3D
            pos, _ = p.getBasePositionAndOrientation(self.sim.robot)
            if self.coord_text_id is not None:
                p.removeUserDebugItem(self.coord_text_id)
            self.coord_text_id = p.addUserDebugText(
                f"x: {pos[0]:.2f}, y: {pos[1]:.2f}",
                [pos[0], pos[1], 0.6],
                textColorRGB=[1, 0, 0],
                textSize=1.5
            )

            self.robot.tick_read_and_write()
            self.sim.tick()
