import math
import random

def clamp01(value):
    if value < 0:
        return 0
    if value > 1:
        return 1
    return value


def sign(value):
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0


def random_normal_distribution():
    theta = math.tau * random.random()
    rho = math.sqrt(-2 * math.log(random.random()))
    return rho * math.cos(theta)
