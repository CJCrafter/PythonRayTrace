from geometry.ray import Vector


class Material:
    def __init__(self, color: Vector = Vector(0, 0, 0), emission: Vector = Vector(0, 0, 0), emission_strength: float = 0.0, smoothness: float = 0.0):
        self.color = color
        self.emission = emission
        self.emission_strength = emission_strength
        self.smoothness = smoothness
