from abc import ABC, abstractmethod

from geometry.ray import Ray, Vector, HitInfo
from material import Material


class Shape(ABC):
    def __init__(self, material: Material):
        self.material = material

    @abstractmethod
    def ray_trace(self, ray: Ray):
        pass


class Sphere(Shape):
    def __init__(self, center: Vector, radius: float, material: Material):
        super().__init__(material)
        self.center = center
        self.radius = radius

    def ray_trace(self, ray: Ray):
        # Compute the vector from the ray's origin to the sphere's center
        oc = ray.origin - self.center

        # Calculate coefficients for the quadratic equation
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius ** 2

        # Calculate the discriminant
        discriminant = b ** 2 - 4 * a * c

        # Check if there is an intersection
        if discriminant < 0:
            return None
        else:
            # Find the closest intersection point
            t = (-b - (discriminant ** 0.5)) / (2.0 * a)
            if t > 0:
                hit_location = ray.origin + ray.direction * t
                normal = (hit_location - self.center).normalize()
                return HitInfo(ray, t, hit_location, normal, self.material)
            return None
