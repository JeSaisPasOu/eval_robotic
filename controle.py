# controls.py
import math
import pybullet as p

class Controle:
    @staticmethod
    def handle_keys(keys):
        mode_rotation = 0
        mode_deplacement = False
        extra_angle = 0
        is_idle = True

        if ord('j') in keys and keys[ord('j')] & p.KEY_IS_DOWN:
            mode_rotation = 1
            is_idle = False

        elif ord('l') in keys and keys[ord('l')] & p.KEY_IS_DOWN:
            mode_rotation = -1
            is_idle = False

        elif ord('z') in keys and keys[ord('z')] & p.KEY_IS_DOWN:
            mode_deplacement = True
            extra_angle = math.pi / 2
            is_idle = False

        elif ord('q') in keys and keys[ord('q')] & p.KEY_IS_DOWN:
            mode_deplacement = True
            extra_angle = -math.pi
            is_idle = False

        elif ord('s') in keys and keys[ord('s')] & p.KEY_IS_DOWN:
            mode_deplacement = True
            extra_angle = -math.pi / 2
            is_idle = False

        elif ord('d') in keys and keys[ord('d')] & p.KEY_IS_DOWN:
            mode_deplacement = True
            extra_angle = 0
            is_idle = False

        return mode_rotation, mode_deplacement, extra_angle, is_idle
