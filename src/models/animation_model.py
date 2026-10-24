"""Физическая модель движения частиц с сопротивлением Стокса"""

import math


class Particle:
    """Сферическая частица, движущаяся в вязкой среде"""

    def __init__(self, radius, mass, velocity, position=0.0):
        """Инициализировать физические параметры частицы"""
        if radius <= 0:
            raise ValueError('Радиус должен быть положительным')
        if mass <= 0:
            raise ValueError('Масса должна быть положительной')

        self.radius = radius
        self.mass = mass
        self.velocity = velocity
        self.position = position

    def drag_force(self, viscosity, fluid_velocity=0.0):
        """Вернуть силу сопротивления Стокса со знаком"""
        if viscosity < 0:
            raise ValueError('Вязкость не может быть отрицательной')

        relative_velocity = self.velocity - fluid_velocity
        return -6.0 * math.pi * viscosity * self.radius * relative_velocity

    def update(self, dt, viscosity, fluid_velocity=0.0, gravity=9.81):
        """Обновить скорость и положение методом Эйлера"""
        if dt < 0:
            raise ValueError('dt не может быть отрицательным')
        if gravity < 0:
            raise ValueError(
                'Ускорение свободного падения не может быть отрицательным'
                )

        force_drag = self.drag_force(viscosity, fluid_velocity)
        acceleration = gravity + force_drag / self.mass

        self.velocity += acceleration * dt
        self.position += self.velocity * dt
