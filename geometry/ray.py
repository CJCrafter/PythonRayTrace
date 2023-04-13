import math

import gamemath


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)
        else:
            raise TypeError("Unsupported operand type(s) for *")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self * (1 / other)

    def to_color(self):
        return (gamemath.clamp01(self.x) * 255, gamemath.clamp01(self.y) * 255, gamemath.clamp01(self.z) * 255)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def magnitude(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self):
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize a zero vector")
        return Vector(self.x / mag, self.y / mag, self.z / mag)

    def reflect(self, normal):
        normal = normal.normalize()
        incoming_ray = self.normalize()
        return incoming_ray - 2 * (incoming_ray.dot(normal)) * normal


class Ray:
    def __init__(self, origin: Vector, direction: Vector):
        self.origin = origin
        self.direction = direction


class HitInfo:
    def __init__(self, ray: Ray, distance: float, hitLocation: Vector, normal: Vector, material):
        self.ray = ray
        self.distance = distance
        self.hitLocation = hitLocation
        self.normal = normal
        self.material = material
