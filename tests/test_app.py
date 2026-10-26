"""Тесты главного приложения (app.py)"""

import tkinter as tk

import pytest

from src.app import ResistanceApp
from src.widgets.controls import SimulationControls


@pytest.fixture
def app(tk_root):
    application = ResistanceApp(tk_root)
    application._stop_animation()
    yield application
    application._stop_animation()


class TestInitialState:
    def test_window_title(self, app):
        assert app.root.title() == 'Силы сопротивления (102)'

    def test_default_physics_parameters(self, app):
        assert app.viscosity == pytest.approx(0.08)
        assert app.fluid_velocity == pytest.approx(0.0)
        assert app.dt == pytest.approx(0.003)
        assert app.frame_delay == 20

    def test_canvas_created(self, app):
        assert isinstance(app.canvas, tk.Canvas)

    def test_controls_created(self, app):
        assert isinstance(app.controls, SimulationControls)


class TestScreenRadius:
    def test_clamped_minimum(self, app):
        class Dummy:
            radius = 0.0000001

        assert app._screen_radius(Dummy()) == pytest.approx(3, abs=0.01)

    def test_clamped_maximum(self, app):
        class Dummy:
            radius = 1.0

        assert app._screen_radius(Dummy()) == pytest.approx(20, abs=0.01)

    def test_within_range(self, app):
        class Dummy:
            radius = 0.003

        result = app._screen_radius(Dummy())

        assert 3 <= result <= 20


class TestStartAndReset:
    def test_start_creates_particles(self, app):
        app.start()

        assert len(app.particles) == 24
        assert app.running is True

        app._stop_animation()

    def test_reset_recreates_particles(self, app):
        app.start()
        first_particles = app.particles
        app._stop_animation()

        app.reset()

        assert app.particles is not first_particles
        assert len(app.particles) == 24

        app._stop_animation()


class TestAnimationControl:
    def test_stop_animation_sets_running_false(self, app):
        app.start()
        app._stop_animation()

        assert app.running is False
        assert app.after_id is None

    def test_stop_animation_is_safe_when_already_stopped(self, app):
        app._stop_animation()
        app._stop_animation()

        assert app.running is False


class TestKeyboardShortcuts:
    def test_restart_shortcut_calls_reset(self, app, monkeypatch):
        called = []
        monkeypatch.setattr(app, 'reset', lambda: called.append(True))

        result = app._on_restart()

        assert called == [True]
        assert result == 'break'

    def test_escape_shortcut_calls_close(self, app, monkeypatch):
        called = []
        monkeypatch.setattr(app, '_close', lambda: called.append(True))

        result = app._on_escape()

        assert called == [True]
        assert result == 'break'


class TestBoundary:
    def test_boundary_y_is_half_of_canvas_height(self, app):
        assert app._boundary_y() == pytest.approx(
            app.canvas.winfo_height() / 2
        )
