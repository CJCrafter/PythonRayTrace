import math
import multiprocessing
import time

import pygame

import gamemath
from geometry.ray import Vector, Ray
from geometry.shape import Sphere
from material import Material

# Set up coordinate system/constants
rays_per_pixel = 100
max_bounce = 10
width = 1000
height = 1000
fov = math.pi / 2  # 90 degrees
distance_to_screen = 1.0


def pixel_to_vector(u: float, v: float):
    u += 0.5
    v += 0.5

    x = (u - width / 2) * (fov / width)
    y = -(v - height / 2) * (fov / height)
    z = distance_to_screen
    return Vector(x, y, z).normalize()


def get_nearest_collision(ray: Ray, geometry: list):
    closest_hit = None
    for shape in geometry:
        current_hit = shape.ray_trace(ray)
        if current_hit is None:
            continue
        if closest_hit is None or closest_hit.distance > current_hit.distance:
            closest_hit = current_hit

    return closest_hit


def random_direction(normal: Vector):
    dir = Vector(gamemath.random_normal_distribution(), gamemath.random_normal_distribution(), gamemath.random_normal_distribution())
    return dir.normalize() * gamemath.sign(normal.dot(dir))


def trace(ray: Ray, geometry):
    incomingLight = Vector(0, 0, 0)
    rayColor = Vector(1, 1, 1)
    is_hit = False

    for i in range(max_bounce):
        hit = get_nearest_collision(ray, geometry)
        if (hit):

            ray.origin = hit.hitLocation
            #ray.direction = ray.direction.reflect(hit.normal)
            ray.direction = random_direction(hit.normal)

            emission = hit.material.emission * hit.material.emission_strength
            strength = hit.normal.dot(ray.direction)
            incomingLight += emission * rayColor
            rayColor *= hit.material.color * strength

            is_hit = True
        else:
            #incomingLight = ray.direction
            break

    return incomingLight, is_hit


def render_portion(start_y, end_y, geometry):
    print(f"Rendering portion {start_y}:{end_y}")
    pixel_data = []
    for pixel_y in range(start_y, end_y):
        for pixel_x in range(width):
            vector = pixel_to_vector(pixel_x, pixel_y)

            vector_color = Vector(0, 0, 0)
            for i in range(rays_per_pixel):
                temp_color, is_hit = trace(Ray(Vector(0, 0, 0), vector), geometry)
                vector_color += temp_color

                if not is_hit:
                    break

            vector_color /= rays_per_pixel
            pixel_data.append(((pixel_x, pixel_y), vector_color.to_color()))

    print(f"Finished portion {start_y}:{end_y}")
    return pixel_data


def main():

    # Define geometry
    geometry = [
        # Sphere(Vector(-20, 20, -100), 50.0, Material(Vector(0, 0, 0), Vector(1, 1, 1), 1)),  # sun

        Sphere(Vector(0, -50, 15), 50, Material(Vector(1, 0, 1))),
        Sphere(Vector(-6, 2, 10), 2.0, Material(Vector(1, 0, 0))),
        Sphere(Vector(0, 2, 10), 2.5, Material(Vector(0, 0, 0), Vector(1, 1, 1), 1.5)),
        Sphere(Vector(6, 2, 10), 2.0, Material(Vector(0, 0, 1))),
    ]

    num_processes = 24  # You can adjust the number of processes based on your CPU
    rows_per_process = height // num_processes

    with multiprocessing.Pool(processes=num_processes) as pool:

        # Import time so we can measure how long it takes to render a frame
        current_unix_time = int(time.time())

        process_args = [(i * rows_per_process, (i + 1) * rows_per_process if i != num_processes - 1 else height, geometry) for i in range(num_processes)]
        results = pool.starmap(render_portion, process_args)

        print(f"Completed render in {int(time.time()) - current_unix_time}s")

        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((width, height))

        for pixel_data in results:
            for (pixel_x, pixel_y), color in pixel_data:
                screen.set_at((pixel_x, pixel_y), color)

        # Update the screen when all processes are done
        pygame.display.update()

        # Run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()


if __name__ == "__main__":
    main()
