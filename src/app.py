"""Графический интерфейс симуляции сопротивления среды"""

import tkinter as tk
from tkinter import messagebox, ttk

from src.models.animation_model import Particle

from src.renderers.renderer import ParticleRenderer
from src.widgets.controls import SimulationControls

class ResistanceApp:
    """Главное окно симуляции"""

    def __init__(self, root):
        """Настроить окно и состояние симуляции"""
        self.root = root
        self.root.title('Силы сопротивления (102)')
        self.root.geometry('1000x650')
        self.root.minsize(750, 450)

        self.particle = None
        self.running = False
        self.after_id = None
        self.viscosity = 0.001
        self.fluid_velocity = 0.0
        self.dt = 0.01
        self.scale = 1000.0

        self._create_widgets()

        self.controls = SimulationControls(
            self.root,
            on_start=self.start,
            on_reset=self.reset,
            )

        self.radius_var = self.controls.radius_var
        self.mass_var = self.controls.mass_var
        self.velocity_var = self.controls.velocity_var
        self.viscosity_var = self.controls.viscosity_var
        self.status_var = self.controls.status_var
        self.renderer = ParticleRenderer(self.canvas)
        self.root.protocol('WM_DELETE_WINDOW', self._close)

    def _create_widgets(self):
        """Создать холст для анимации"""
        self.canvas = tk.Canvas(
            self.root,
            background='white',
            highlightthickness=1,
            highlightbackground='#cccccc',
        )
        self.canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=10,
        )

    def start(self):
        """Создать частицу и запустить анимацию"""
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.particle = None
        self.renderer.clear()

        try:
            radius = self.radius_var.get()
            mass = self.mass_var.get()
            velocity = self.velocity_var.get()
            viscosity = self.viscosity_var.get()

            if not 0 < radius <= 0.01:
                raise ValueError(
                    'Радиус должен быть больше 0 и не превышать 0.01 м.'
                )

            if not 0 < mass <= 1:
                raise ValueError(
                    'Масса должна быть больше 0 и не превышать 1 кг.'
                )

            if not 0 <= viscosity <= 10:
                raise ValueError(
                    'Вязкость должна быть от 0 до 10 Па·с.'
                )

            if abs(velocity) > 100:
                raise ValueError(
                    'Начальная скорость должна быть от -100 до 100 м/с.'
                )

            self.particle = Particle(
                radius=radius,
                mass=mass,
                velocity=velocity,
            )
            self.viscosity = viscosity
        except (ValueError, tk.TclError) as error:
            messagebox.showerror('Ошибка параметров', str(error))
            return

        self.running = True
        self._animate()

    
    def _animate(self):
        """Выполнить шаг физики и нарисовать частицу"""
        if not self.running or self.particle is None:
            return

        bottom_y = self.canvas.winfo_height() - 30
        center_x = self.canvas.winfo_width() / 2

        self.particle.update(
            dt=self.dt,
            viscosity=self.viscosity,
            fluid_velocity=self.fluid_velocity,
        )

        y = 30 + self.particle.position * self.scale

        if y >= bottom_y:
            y = bottom_y
            self.running = False

        self.renderer.clear()
        self.renderer.draw_ground()
        self.renderer.draw_particle(
            x=center_x,
            y=y,
            radius=self.particle.radius,
        )

        self.status_var.set(
            f'Шаг времени: {self.dt:.3f} с\n'
            f'Положение: {self.particle.position:.4f} м\n'
            f'Скорость: {self.particle.velocity:.4f} м/с\n'
            f'Сила сопротивления: '
            f'{self.particle.drag_force(self.viscosity):.6f} Н'
        )

        if self.running:
            self.after_id = self.root.after(10, self._animate)

    def reset(self):
        """Остановить анимацию и вернуть исходные параметры"""
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.renderer.clear()
        self.particle = None

        self.radius_var.set(0.001)
        self.mass_var.set(0.01)
        self.velocity_var.set(0.0)
        self.viscosity_var.set(0.001)

        self.status_var.set('Задай параметры и нажми «Запустить»')

    def _close(self):
        """Закрыть приложение"""
        self.reset()
        self.root.destroy()
