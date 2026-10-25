"""Физическая модель движения сферических частиц в двух средах"""

import math
import random


class Particle:
    """Сферическая частица, движущаяся вертикально вниз"""

    def __init__(
        self,
        radius,
        mass,
        velocity=0.0,
        position=0.0,
        in_resistive_medium=False,
    ):
        if not math.isfinite(radius) or radius <= 0:
            raise ValueError('Радиус должен быть положительным числом')
        if not math.isfinite(mass) or mass <= 0:
            raise ValueError('Масса должна быть положительной')
        if not math.isfinite(velocity) or not math.isfinite(position):
            raise ValueError('Скорость и положение должны быть конечными числами')

        self.radius = float(radius)
        self.mass = float(mass)
        self.velocity = float(velocity)
        self.position = float(position)
        self.in_resistive_medium = bool(in_resistive_medium)

    def drag_force(
        self,
        viscosity,
        fluid_velocity=0.0,
        fluid_density=1000.0,
    ):
        """Сила сопротивления среды ~ r²"""
        if not self.in_resistive_medium:
            return 0.0

        relative_velocity = self.velocity - fluid_velocity
        speed = abs(relative_velocity)

        if speed == 0.0:
            return 0.0

        area = math.pi * (self.radius ** 2)

        reynolds = (
            2.0 * self.radius * fluid_density * speed / viscosity
            if viscosity > 0.0
            else math.inf
        )

        if reynolds < 1e-6:
            magnitude = 6.0 * math.pi * viscosity * self.radius * speed
        else:
            if reynolds < 1000.0:
                coefficient = (24.0 / reynolds) * (1.0 + 0.15 * (reynolds ** 0.687))
            else:
                coefficient = 0.44

            magnitude = 0.5 * fluid_density * coefficient * area * (speed ** 2)

        return -math.copysign(magnitude, relative_velocity)

    def update(
        self,
        dt,
        viscosity,
        fluid_velocity=0.0,
        gravity=9.81,
        fluid_density=1000.0,
    ):
        """Обновление с учётом инерции m ~ r³"""
        force_drag = self.drag_force(
            viscosity=viscosity,
            fluid_velocity=fluid_velocity,
            fluid_density=fluid_density,
        )

        acceleration = gravity + (force_drag / self.mass)

        self.velocity += acceleration * dt
        self.position += self.velocity * dt


def create_particles(
    initial_velocity=0.3,
    base_radius=0.003,
    base_mass=0.02,
    count=24,
):
    """Разноразмерные частицы с одинаковой начальной скоростью"""
    size_factors = [0.3 + i * (1.5 / (count - 1)) for i in range(count)]
    random.shuffle(size_factors)

    particles = []

    for size in size_factors:
        radius = base_radius * size
        mass = base_mass * (size ** 3)

        particles.append(
            Particle(
                radius=radius,
                mass=mass,
                velocity=initial_velocity,
                position=0.0,
                in_resistive_medium=False,
            )
        )

    return particles
