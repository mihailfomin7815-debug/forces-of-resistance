"""Тесты отрисовки (renderer.py)"""

import tkinter as tk

import pytest

from src.renderers.renderer import ParticleRenderer


@pytest.fixture
def canvas(tk_root):
    cv = tk.Canvas(tk_root, width=400, height=300)
    cv.pack()
    tk_root.update_idletasks()
    return cv


class TestClear:
    def test_clear_removes_all_items(self, canvas):
        renderer = ParticleRenderer(canvas)

        canvas.create_rectangle(0, 0, 10, 10)
        canvas.create_oval(0, 0, 5, 5)
        assert len(canvas.find_all()) > 0

        renderer.clear()

        assert len(canvas.find_all()) == 0


class TestDrawEnvironment:
    def test_creates_two_rectangles(self, canvas):
        renderer = ParticleRenderer(canvas)

        renderer.draw_environment(boundary_y=150)

        items = canvas.find_withtag('environment')
        assert len(items) == 2

    def test_top_rectangle_is_black(self, canvas):
        renderer = ParticleRenderer(canvas)
        renderer.draw_environment(boundary_y=150)

        top_item = canvas.find_withtag('environment')[0]

        assert canvas.itemcget(top_item, 'fill') == '#000000'

    def test_bottom_rectangle_is_grey(self, canvas):
        renderer = ParticleRenderer(canvas)
        renderer.draw_environment(boundary_y=150)

        bottom_item = canvas.find_withtag('environment')[1]

        assert canvas.itemcget(bottom_item, 'fill') == '#6e6e6e'

    def test_rectangles_split_at_boundary(self, canvas):
        renderer = ParticleRenderer(canvas)
        boundary_y = 120

        renderer.draw_environment(boundary_y=boundary_y)

        items = canvas.find_withtag('environment')
        top_coords = canvas.coords(items[0])
        bottom_coords = canvas.coords(items[1])

        assert top_coords[1] == pytest.approx(0)
        assert top_coords[3] == pytest.approx(boundary_y)
        assert bottom_coords[1] == pytest.approx(boundary_y)


class TestDrawParticle:
    def test_creates_oval_with_particle_tag(self, canvas):
        renderer = ParticleRenderer(canvas)

        renderer.draw_particle(x=50, y=60, radius=0.003)

        assert len(canvas.find_withtag('particle')) == 1

    def test_particle_has_transparent_fill_and_white_outline(self, canvas):
        renderer = ParticleRenderer(canvas)

        renderer.draw_particle(x=50, y=60, radius=0.003)

        item = canvas.find_withtag('particle')[0]

        assert canvas.itemcget(item, 'outline') == '#ffffff'
        assert canvas.itemcget(item, 'fill') == ''

    def test_radius_is_clamped_to_minimum(self, canvas):
        renderer = ParticleRenderer(canvas)

        renderer.draw_particle(x=0, y=0, radius=0.0000001)

        x0, y0, x1, y1 = canvas.coords(canvas.find_withtag('particle')[0])
        screen_radius = (x1 - x0) / 2

        assert screen_radius == pytest.approx(3, abs=0.5)

    def test_radius_is_clamped_to_maximum(self, canvas):
        renderer = ParticleRenderer(canvas)

        renderer.draw_particle(x=0, y=0, radius=1.0)

        x0, y0, x1, y1 = canvas.coords(canvas.find_withtag('particle')[0])
        screen_radius = (x1 - x0) / 2

        assert screen_radius == pytest.approx(20, abs=0.5)

    def test_particle_centered_on_given_coordinates(self, canvas):
        renderer = ParticleRenderer(canvas)

        x, y, radius = 80, 90, 0.003
        renderer.draw_particle(x=x, y=y, radius=radius)

        x0, y0, x1, y1 = canvas.coords(canvas.find_withtag('particle')[0])

        assert (x0 + x1) / 2 == pytest.approx(x, abs=0.5)
        assert (y0 + y1) / 2 == pytest.approx(y, abs=0.5)
