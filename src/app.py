"""Главное окно симуляции сил сопротивления"""

import tkinter as tk

from src.models.animation_model import create_particles
from src.renderers.renderer import ParticleRenderer
from src.widgets.controls import SimulationControls


class ResistanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Силы сопротивления (102)')
        self.root.geometry('600x580')
        self.root.minsize(400, 450)

        self.particles = []
        self.running = False
        self.after_id = None

        self.viscosity = 0.08
        self.fluid_velocity = 0.0
        self.resistance_factor = 1.0

        self.dt = 0.003
        self.frame_delay = 20

        self.position_scale = 140.0
        self.top_margin = 30

        self._create_widgets()
        self.renderer = ParticleRenderer(self.canvas)

        self.controls = SimulationControls(
            self.root,
            on_start=self.start,
            on_reset=self.reset,
            on_resistance_change=self._set_resistance,
        )

        self.root.bind_all('<KeyPress-r>', self._on_restart)
        self.root.bind_all('<KeyPress-R>', self._on_restart)
        self.root.bind_all('<Escape>', self._on_escape)

        self.root.protocol('WM_DELETE_WINDOW', self._close)
        self.root.after(100, self._start_automatically)

    def _create_widgets(self):
        self.canvas = tk.Canvas(
            self.root,
            background='#000000',
            highlightthickness=0,
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _boundary_y(self):
        return self.canvas.winfo_height() / 2

    @staticmethod
    def _screen_radius(particle):
        return max(3, min(20, particle.radius * 4000))

    def _start_automatically(self):
        self.renderer.clear()
        self.renderer.draw_environment(self._boundary_y())
        self.start()

    def start(self):
        self._stop_animation()

        self.particles = create_particles(
            initial_velocity=0.3,
            base_radius=0.003,
            base_mass=0.02,
            count=24,
        )

        self.running = True
        self._animate()

    def _set_resistance(self, percent):
        """Устанавливает сопротивление в процентах"""
        self.resistance_factor = float(percent) / 100.0

    def _animate(self):
        self.after_id = None

        if not self.running or not self.particles:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width <= 1 or height <= 1:
            self.after_id = self.root.after(self.frame_delay, self._animate)
            return

        boundary_y = self._boundary_y()
        boundary_position = max(
            0.0,
            (boundary_y - self.top_margin) / self.position_scale,
        )

        for particle in self.particles:
            if (
                not particle.in_resistive_medium
                and particle.position >= boundary_position
            ):
                particle.in_resistive_medium = True

            particle.update(
                dt=self.dt,
                viscosity=self.viscosity,
                fluid_velocity=self.fluid_velocity,
                resistance_factor=self.resistance_factor,
            )

            screen_r = self._screen_radius(particle)
            max_pos = (
                height - screen_r - 2 - self.top_margin
            ) / self.position_scale

            if particle.position >= max_pos:
                particle.position = max_pos
                if particle.velocity > 0:
                    particle.velocity = -abs(particle.velocity) * 0.75

        self.renderer.clear()
        self.renderer.draw_environment(boundary_y)

        spacing = width / (len(self.particles) + 1)
        for index, particle in enumerate(self.particles):
            x = spacing * (index + 1)
            screen_r = self._screen_radius(particle)

            y = self.top_margin + particle.position * self.position_scale
            y = max(screen_r, min(y, height - screen_r - 2))

            self.renderer.draw_particle(
                x=x,
                y=y,
                radius=particle.radius,
            )

        self.after_id = self.root.after(self.frame_delay, self._animate)

    def _stop_animation(self):
        self.running = False
        if self.after_id is not None:
            try:
                self.root.after_cancel(self.after_id)
            except tk.TclError:
                pass
            self.after_id = None

    def reset(self):
        self._stop_animation()
        self.start()

    def _on_restart(self, event=None):
        self.reset()
        return 'break'

    def _on_escape(self, event=None):
        self._close()
        return 'break'

    def _close(self):
        self._stop_animation()
        self.root.destroy()


def main():
    root = tk.Tk()
    ResistanceApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
