import math

from constants import *
import pybullet as p
DEFAULT_COMPUTE_IK_SIGN = -1

# Given the sizes (a, b, c) of the 3 sides of a triangle, returns the angle between a and b using the alKashi theorem.
def alKashi(a, b, c, sign=1):
    if a * b == 0:
        print("WARNING a or b is null in AlKashi")
        return 0
    # Note : to get the other altenative, simply change the sign of the return :
    return sign * math.acos(min(1, max(-1, (a**2 + b**2 - c**2) / (2 * a * b))))


# Computes the direct kinematics of a leg in the leg's frame
# Given the angles (theta1, theta2, theta3) of a limb with 3 rotational axes separated by the distances (l1, l2, l3),
# returns the destination point (x, y, z)
def computeDK(
    theta1,
    theta2,
    theta3,
    l1=constL1,
    l2=constL2,
    l3=constL3,
    use_rads=USE_RADS_INPUT,
    use_mm=USE_MM_OUTPUT,
):
    angle_unit = 1
    dist_unit = 1
    if not (use_rads):
        angle_unit = math.pi / 180.0
    if use_mm:
        dist_unit = 1000
    theta1 = THETA1_MOTOR_SIGN * theta1 * angle_unit
    theta2 = (THETA2_MOTOR_SIGN * theta2 - theta2Correction) * angle_unit
    theta3 = (THETA3_MOTOR_SIGN * theta3 - theta3Correction) * angle_unit
    # print(
    #     "corrected angles={}, {}, {}".format(
    #         theta1 * (1.0 / angle_unit),
    #         theta2 * (1.0 / angle_unit),
    #         theta3 * (1.0 / angle_unit),
    #     )
    # )

    planContribution = l1 + l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3)

    x = math.cos(theta1) * planContribution * dist_unit
    y = math.sin(theta1) * planContribution * dist_unit
    z = -(l2 * math.sin(theta2) + l3 * math.sin(theta2 + theta3)) * dist_unit

    return [x, y, z]


def computeDKDetailed(
    theta1,
    theta2,
    theta3,
    l1=constL1,
    l2=constL2,
    l3=constL3,
    use_rads=USE_RADS_INPUT,
    use_mm=USE_MM_OUTPUT,
):
    theta1_verif = theta1
    theta2_verif = theta2
    theta3_verif = theta3
    angle_unit = 1
    dist_unit = 1
    if not (use_rads):
        angle_unit = math.pi / 180.0
    if use_mm:
        dist_unit = 1000
    theta1 = THETA1_MOTOR_SIGN * theta1 * angle_unit
    theta2 = (THETA2_MOTOR_SIGN * theta2 - theta2Correction) * angle_unit
    theta3 = (THETA3_MOTOR_SIGN * theta3 - theta3Correction) * angle_unit

    print(
        "corrected angles={}, {}, {}".format(
            theta1 * (1.0 / angle_unit),
            theta2 * (1.0 / angle_unit),
            theta3 * (1.0 / angle_unit),
        )
    )

    planContribution = l1 + l2 * math.cos(theta2) + l3 * math.cos(theta2 + theta3)

    x = math.cos(theta1) * planContribution
    y = math.sin(theta1) * planContribution
    z = -(l2 * math.sin(theta2) + l3 * math.sin(theta2 + theta3))

    p0 = [0, 0, 0]
    p1 = [l1 * math.cos(theta1) * dist_unit, l1 * math.sin(theta1) * dist_unit, 0]
    p2 = [
        (l1 + l2 * math.cos(theta2)) * math.cos(theta1) * dist_unit,
        (l1 + l2 * math.cos(theta2)) * math.sin(theta1) * dist_unit,
        -l2 * math.sin(theta2) * dist_unit,
    ]
    p3 = [x * dist_unit, y * dist_unit, z * dist_unit]
    p3_verif = computeDK(
        theta1_verif, theta2_verif, theta3_verif, l1, l2, l3, use_rads, use_mm
    )
    if (p3[0] != p3_verif[0]) or (p3[1] != p3_verif[1]) or (p3[2] != p3_verif[2]):
        print(
            "ERROR: the DK function is broken!!! p3 = {}, p3_verif = {}".format(
                p3, p3_verif
            )
        )

    return [p0, p1, p2, p3]


# Computes the inverse kinematics of a leg in the leg's frame
# Given the destination point (x, y, z) of a limb with 3 rotational axes separated by the distances (l1, l2, l3),
# returns the angles to apply to the 3 axes
def computeIK(
    x,
    y,
    z,
    l1=constL1,
    l2=constL2,
    l3=constL3,
    verbose=False,
    use_rads=USE_RADS_OUTPUT,
    sign=DEFAULT_COMPUTE_IK_SIGN,
    use_mm=USE_MM_INPUT,
):
    dist_unit = 1
    if use_mm:
        dist_unit = 0.001
    x = x * dist_unit
    y = y * dist_unit
    z = z * dist_unit

    # theta1 is simply the angle of the leg in the X/Y plane. We have the first angle we wanted.
    if y == 0 and x == 0:
        # Taking care of this singularity (leg right on top of the first rotational axis)
        theta1 = 0
    else:
        theta1 = math.atan2(y, x)

    # Distance between the second motor and the projection of the end of the leg on the X/Y plane
    xp = math.sqrt(x * x + y * y) - l1
    # if xp < 0:
    #     print("Destination point too close")
    #     xp = 0

    # Distance between the second motor arm and the end of the leg
    d = math.sqrt(math.pow(xp, 2) + math.pow(z, 2))
    # if d > l2 + l3:
    #     print("Destination point too far away")
    #     d = l2 + l3

    # Knowing l2, l3 and d, theta1 and theta2 can be computed using the Al Kashi law
    # There are 2 solutions for most of the points, forcing a convention here
    theta2 = alKashi(l2, d, l3, sign=sign) - Z_DIRECTION * math.atan2(z, xp)
    theta3 = math.pi + alKashi(l2, l3, d, sign=sign)

    if use_rads:
        result = [
            angleRestrict(THETA1_MOTOR_SIGN * theta1, use_rads=use_rads),
            angleRestrict(
                THETA2_MOTOR_SIGN * (theta2 + theta2Correction), use_rads=use_rads
            ),
            angleRestrict(
                THETA3_MOTOR_SIGN * (theta3 + theta3Correction), use_rads=use_rads
            ),
        ]

    else:
        result = [
            angleRestrict(THETA1_MOTOR_SIGN * math.degrees(theta1), use_rads=use_rads),
            angleRestrict(
                THETA2_MOTOR_SIGN * (math.degrees(theta2) + theta2Correction),
                use_rads=use_rads,
            ),
            angleRestrict(
                THETA3_MOTOR_SIGN * (math.degrees(theta3) + theta3Correction),
                use_rads=use_rads,
            ),
        ]
    if verbose:
        print(
            "Asked IK for x={}, y={}, z={}\n, --> theta1={}, theta2={}, theta3={}".format(
                x,
                y,
                z,
                result[0],
                result[1],
                result[2],
            )
        )

    return result


def angleRestrict(angle, use_rads=False):
    if use_rads:
        return modulopi(angle)
    else:
        return modulo180(angle)


# Takes an angle that's between 0 and 360 and returns an angle that is between -180 and 180
def modulo180(angle):
    if -180 < angle < 180:
        return angle

    angle = angle % 360
    if angle > 180:
        return -360 + angle

    return angle


def modulopi(angle):
    if -math.pi < angle < math.pi:
        return angle

    angle = angle % (math.pi * 2)
    if angle > math.pi:
        return -math.pi * 2 + angle

    return angle

def rotaton_2D(x, y, z, angle):
   
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
 
    x_new = cos_theta * x - sin_theta * y
    y_new = sin_theta * x + cos_theta * y
 
    return [x_new, y_new, z]

def triangle(x, z, h, w, t, leg_id=None):

    keys = p.getKeyboardEvents()
    extra_angle = 0 
    if ord('d') in keys and keys[ord('d')] & p.KEY_IS_DOWN:
        extra_angle = 0
    if ord('q') in keys and keys[ord('q')] & p.KEY_IS_DOWN:
        extra_angle = -math.pi
    if ord('z') in keys and keys[ord('z')] & p.KEY_IS_DOWN:
        extra_angle = math.pi/2
    if ord('s') in keys and keys[ord('s')] & p.KEY_IS_DOWN:
        extra_angle = -math.pi/2
    
    phase = t % 2
 
    if phase < 1:
        ratio = phase
        y1 = w/2
        y2 = -w/2
        z1 = z
        z2 = z
    elif phase < 1.5:
        ratio = (phase -1) * 2
        y1 = -w/2
        y2 = 0
        z1 = z
        z2 = z + h
    else:
        ratio = (phase -1.5) * 2
        y1 = 0
        y2 = w/2
        z1 = z + h
        z2 = z
    
    target_y = interpol(y1, y2, ratio)
    target_z = interpol(z1, z2, ratio)
    if leg_id is None:
        alpha = computeIK(x, target_y, target_z)
    else:
        alpha= computeIKOriented(x, target_y, target_z, leg_id, extra_angle)
        
    return alpha

def interpol(p1, p2, ratio):
    return p1 + ratio * (p2-p1)

def computeIKOrientedperso(x, y, z,leg_id,sens):
    offset_x= 0.2
    offset_y= 0
    offset_z= -0.05
    if sens == 1 :
        new_x, new_y, new_z= rotaton_2D(x, y, z,-LEG_ANGLES[leg_id-1])
    elif sens == 2:
        new_x, new_y, new_z= rotaton_2D(x, y, z,-LEG_ANGLES[leg_id-1])
        new_x = -new_x
        new_y= -new_y
    elif sens == 3 :
        new_x, new_y, new_z= rotaton_2D(x, y, z,-LEG_ANGLES[leg_id-1]+math.pi/2)
    elif sens == 4:
        new_x, new_y, new_z= rotaton_2D(x, y, z,-LEG_ANGLES[leg_id-1]+math.pi/2)
        new_x = -new_x
        new_y= -new_y
    else:
        new_x, new_y, new_z= rotaton_2D(0, 0, z,-LEG_ANGLES[leg_id-1])

    return computeIK(new_x+ offset_x, new_y+ offset_y, new_z+ offset_z)

def computeIKOriented(x, y, z,leg_id,angle):
    offset_x= 0.2
    offset_y= 0
    offset_z= -0.05
    new_x, new_y, new_z= rotaton_2D(x, y, z,-LEG_ANGLES[leg_id-1]+angle)
    
    return computeIK(new_x+ offset_x, new_y+ offset_y, new_z+ offset_z)