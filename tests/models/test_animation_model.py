"""Тесты физической модели частиц (animation_model.py)"""

import math

import pytest

from src.models.animation_model import Particle, create_particles



class TestParticleInit:
    def test_valid_particle_created(self):
        p = Particle(radius=0.01, mass=0.05, velocity=1.0, position=2.0)

        assert p.radius == pytest.approx(0.01)
        assert p.mass == pytest.approx(0.05)
        assert p.velocity == pytest.approx(1.0)
        assert p.position == pytest.approx(2.0)
        assert p.in_resistive_medium is False

    def test_default_values(self):
        p = Particle(radius=0.01, mass=0.05)

        assert p.velocity == 0.0
        assert p.position == 0.0
        assert p.in_resistive_medium is False

    @pytest.mark.parametrize('radius', [0, -1, -0.001])
    def test_invalid_radius_raises(self, radius):
        with pytest.raises(ValueError):
            Particle(radius=radius, mass=1.0)

    @pytest.mark.parametrize('mass', [0, -1, -0.5])
    def test_invalid_mass_raises(self, mass):
        with pytest.raises(ValueError):
            Particle(radius=1.0, mass=mass)

    def test_non_finite_radius_raises(self):
        with pytest.raises(ValueError):
            Particle(radius=math.nan, mass=1.0)
        with pytest.raises(ValueError):
            Particle(radius=math.inf, mass=1.0)

    def test_non_finite_mass_raises(self):
        with pytest.raises(ValueError):
            Particle(radius=1.0, mass=math.nan)

    def test_non_finite_velocity_raises(self):
        with pytest.raises(ValueError):
            Particle(radius=1.0, mass=1.0, velocity=math.inf)

    def test_non_finite_position_raises(self):
        with pytest.raises(ValueError):
            Particle(radius=1.0, mass=1.0, position=math.nan)


class TestDragForce:
    def test_no_drag_outside_resistive_medium(self):
        p = Particle(radius=0.01, mass=0.05, velocity=2.0,
                     in_resistive_medium=False)

        assert p.drag_force(viscosity=0.1) == 0.0

    def test_no_drag_when_speed_is_zero(self):
        p = Particle(radius=0.01, mass=0.05, velocity=0.0,
                     in_resistive_medium=True)

        assert p.drag_force(viscosity=0.1, fluid_velocity=0.0) == 0.0

    def test_drag_opposes_downward_motion(self):
        p = Particle(radius=0.01, mass=0.05, velocity=2.0,
                     in_resistive_medium=True)

        force = p.drag_force(viscosity=0.1)

        assert force < 0.0

    def test_drag_opposes_upward_motion(self):
        p = Particle(radius=0.01, mass=0.05, velocity=-2.0,
                     in_resistive_medium=True)

        force = p.drag_force(viscosity=0.1)

        assert force > 0.0

    def test_drag_force_is_finite(self):
        p = Particle(radius=0.005, mass=0.01, velocity=5.0,
                     in_resistive_medium=True)

        force = p.drag_force(viscosity=0.08)

        assert math.isfinite(force)

    def test_zero_viscosity_uses_high_reynolds_branch(self):
        """При viscosity=0 Re -> inf, коэффициент сопротивления = 0.44"""
        radius = 0.01
        velocity = 3.0
        fluid_density = 1000.0

        p = Particle(radius=radius, mass=0.05, velocity=velocity,
                     in_resistive_medium=True)

        force = p.drag_force(viscosity=0.0, fluid_density=fluid_density)

        area = math.pi * radius ** 2
        expected_magnitude = 0.5 * fluid_density * 0.44 * area * velocity ** 2

        assert force == pytest.approx(-expected_magnitude, rel=1e-6)

    def test_larger_radius_increases_drag_force_magnitude(self):
        """
        При одинаковой скорости и высоком Re (Cd=const)
        сила сопротивления растёт с площадью сечения (~ r^2)
        """
        velocity = 10.0
        viscosity = 0.001

        small = Particle(radius=0.01, mass=0.02, velocity=velocity,
                          in_resistive_medium=True)
        large = Particle(radius=0.02, mass=0.02, velocity=velocity,
                          in_resistive_medium=True)

        force_small = small.drag_force(viscosity=viscosity)
        force_large = large.drag_force(viscosity=viscosity)

        assert abs(force_large) > abs(force_small)

    def test_no_relative_motion_with_moving_fluid(self):
        """Частица, движущаяся со скоростью среды, не испытывает сопротивления"""
        p = Particle(radius=0.01, mass=0.02, velocity=3.0,
                     in_resistive_medium=True)

        force = p.drag_force(viscosity=0.1, fluid_velocity=3.0)

        assert force == 0.0

    def test_zero_resistance_factor_disables_drag(self):
        p = Particle(
            radius=0.01,
            mass=0.05,
            velocity=2.0,
            in_resistive_medium=True,
        )

        force = p.drag_force(
            viscosity=0.1,
            resistance_factor=0.0,
        )

        assert force == 0.0

    def test_double_resistance_factor_doubles_drag(self):
        p = Particle(
            radius=0.01,
            mass=0.05,
            velocity=2.0,
            in_resistive_medium=True,
        )

        normal_force = p.drag_force(
            viscosity=0.1,
            resistance_factor=1.0,
        )
        double_force = p.drag_force(
            viscosity=0.1,
            resistance_factor=2.0,
        )

        assert double_force == pytest.approx(
            2.0 * normal_force
        )


class TestUpdate:
    def test_update_without_resistance_matches_free_fall(self):
        p = Particle(radius=0.01, mass=0.02, velocity=0.0, position=0.0,
                     in_resistive_medium=False)

        dt = 0.01
        gravity = 9.81

        p.update(dt=dt, viscosity=0.1, gravity=gravity)

        expected_velocity = gravity * dt
        expected_position = expected_velocity * dt

        assert p.velocity == pytest.approx(expected_velocity)
        assert p.position == pytest.approx(expected_position)

    def test_update_with_resistance_slows_down_compared_to_free_fall(self):
        free = Particle(radius=0.01, mass=0.02, velocity=5.0,
                         in_resistive_medium=False)
        resisted = Particle(radius=0.01, mass=0.02, velocity=5.0,
                             in_resistive_medium=True)

        dt = 0.01

        free.update(dt=dt, viscosity=0.1)
        resisted.update(dt=dt, viscosity=0.1)

        assert resisted.velocity < free.velocity

    def test_larger_particle_loses_less_relative_velocity(self):
        """
        Инерция более массивной частицы сильнее
        противостоит торможению в вязкой среде
        """
        small = Particle(radius=0.003, mass=0.02 * (0.5 ** 3), velocity=5.0,
                          in_resistive_medium=True)
        large = Particle(radius=0.006, mass=0.02 * (1.0 ** 3), velocity=5.0,
                          in_resistive_medium=True)

        dt = 0.01
        viscosity = 0.5

        small.update(dt=dt, viscosity=viscosity)
        large.update(dt=dt, viscosity=viscosity)

        small_loss = 5.0 - small.velocity
        large_loss = 5.0 - large.velocity

        assert large_loss < small_loss

    
    def test_update_with_zero_resistance_matches_free_fall(self):
        p = Particle(
            radius=0.01,
            mass=0.05,
            velocity=5.0,
            in_resistive_medium=True,
        )

        dt = 0.01
        gravity = 9.81

        p.update(
            dt=dt,
            viscosity=0.1,
            gravity=gravity,
            resistance_factor=0.0,
        )

        assert p.velocity == pytest.approx(
            5.0 + gravity * dt
        )



class TestCreateParticles:
    def test_default_count(self):
        particles = create_particles()

        assert len(particles) == 24

    def test_custom_count(self):
        particles = create_particles(count=10)

        assert len(particles) == 10

    def test_all_particles_have_equal_initial_velocity(self):
        initial_velocity = 0.7
        particles = create_particles(initial_velocity=initial_velocity, count=12)

        for p in particles:
            assert p.velocity == pytest.approx(initial_velocity)

    def test_particles_start_at_zero_position(self):
        particles = create_particles(count=8)

        for p in particles:
            assert p.position == 0.0

    def test_particles_start_outside_resistive_medium(self):
        particles = create_particles(count=8)

        for p in particles:
            assert p.in_resistive_medium is False

    def test_radii_are_distinct(self):
        particles = create_particles(count=16)

        radii = {p.radius for p in particles}

        assert len(radii) == 16

    def test_mass_scales_with_cube_of_relative_radius(self):
        base_radius = 0.004
        base_mass = 0.03
        particles = create_particles(
            base_radius=base_radius,
            base_mass=base_mass,
            count=10,
        )

        for p in particles:
            size_factor = p.radius / base_radius
            expected_mass = base_mass * size_factor ** 3

            assert p.mass == pytest.approx(expected_mass)

    def test_particles_are_particle_instances(self):
        particles = create_particles(count=5)

        assert all(isinstance(p, Particle) for p in particles)

    