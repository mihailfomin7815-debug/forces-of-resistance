"""Тесты физической модели движения частиц"""

import math
import unittest

from src.models.animation_model import Particle


class TestParticle(unittest.TestCase):
    """Проверить поведение частицы"""

    def test_initial_values(self):
        """Параметры частицы сохраняются при создании"""
        particle = Particle(radius=0.01, mass=0.1, velocity=2.0)

        self.assertEqual(particle.radius, 0.01)
        self.assertEqual(particle.mass, 0.1)
        self.assertEqual(particle.velocity, 2.0)
        self.assertEqual(particle.position, 0.0)

    def test_invalid_radius(self):
        """Радиус должен быть положительным"""
        with self.assertRaises(ValueError):
            Particle(radius=0, mass=0.1, velocity=1.0)

    def test_invalid_mass(self):
        """Масса должна быть положительной"""
        with self.assertRaises(ValueError):
            Particle(radius=0.01, mass=-1.0, velocity=1.0)

    def test_stokes_drag_force(self):
        """Сила Стокса пропорциональна радиусу и относительной скорости"""
        particle = Particle(radius=0.01, mass=0.1, velocity=2.0)

        force = particle.drag_force(viscosity=0.001)

        expected = -6.0 * math.pi * 0.001 * 0.01 * 2.0
        self.assertAlmostEqual(force, expected)

    def test_drag_force_with_moving_fluid(self):
        """Сопротивление зависит от скорости частицы относительно среды"""
        particle = Particle(radius=0.01, mass=0.1, velocity=3.0)

        force = particle.drag_force(
            viscosity=0.001,
            fluid_velocity=1.0,
        )

        expected = -6.0 * math.pi * 0.001 * 0.01 * 2.0
        self.assertAlmostEqual(force, expected)

    def test_particle_slows_down_without_gravity(self):
        """Сопротивление уменьшает скорость движущейся частицы"""
        particle = Particle(radius=0.01, mass=0.1, velocity=2.0)

        particle.update(dt=0.01, viscosity=0.001, gravity=0.0)

        self.assertLess(particle.velocity, 2.0)
        self.assertGreater(particle.velocity, 0.0)


if __name__ == "__main__":
    unittest.main()
