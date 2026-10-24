"""Графический интерфейс симуляции сопротивления среды"""

import tkinter as tk
from tkinter import messagebox, ttk

from src.models.animation_model import Particle

from src.renderers.renderer import ParticleRenderer

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
        self.renderer = ParticleRenderer(self.canvas)
        self.root.protocol('WM_DELETE_WINDOW', self._close)

    def _create_widgets(self):
        """Создать холст и панель управления"""
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

        controls = ttk.Frame(self.root, padding=10)
        controls.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(
            controls,
            text='Силы сопротивления',
            font=('Arial', 14, 'bold'),
        ).pack(pady=(0, 12))

        self.radius_var = tk.DoubleVar(value=0.001)
        self.mass_var = tk.DoubleVar(value=0.01)
        self.velocity_var = tk.DoubleVar(value=0.0)
        self.viscosity_var = tk.DoubleVar(value=0.001)

        self._add_field(controls, 'Радиус частицы (м)', self.radius_var)
        self._add_field(controls, 'Масса частицы (кг)', self.mass_var)
        self._add_field(
            controls,
            'Начальная скорость (м/с)',
            self.velocity_var,
        )
        self._add_field(
            controls,
            'Вязкость среды (Па·с)',
            self.viscosity_var,
        )

        ttk.Button(
            controls,
            text='Запустить',
            command=self.start,
        ).pack(fill=tk.X, pady=(12, 4))

        ttk.Button(
            controls,
            text='Сбросить',
            command=self.reset,
        ).pack(fill=tk.X, pady=4)

        self.status_var = tk.StringVar(
            value='Задай параметры и нажми «Запустить»'
        )
        ttk.Label(
            controls,
            textvariable=self.status_var,
            wraplength=210,
        ).pack(pady=10)

    @staticmethod
    def _add_field(parent, label, variable):
        """Добавить поле ввода параметра"""
        ttk.Label(parent, text=label).pack(anchor='w')
        ttk.Entry(parent, textvariable=variable).pack(
            fill=tk.X,
            pady=(0, 8),
        )

    def start(self):
        """Создать частицу и запустить анимацию"""
        self.reset()

        try:
            radius = self.radius_var.get()
            mass = self.mass_var.get()
            velocity = self.velocity_var.get()
            viscosity = self.viscosity_var.get()

            if radius <= 0 or mass <= 0 or viscosity < 0:
                raise ValueError(
                    'Радиус и масса должны быть положительными, '
                    'вязкость — неотрицательной.'
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
        """Выполнить один шаг физики и нарисовать частицу"""
        if not self.running or self.particle is None:
            return

        self.particle.update(
            dt=self.dt,
            viscosity=self.viscosity,
            fluid_velocity=self.fluid_velocity,
        )

        self.renderer.clear()

        center_x = self.canvas.winfo_width() / 2
        bottom_y = self.canvas.winfo_height() - 30

        y = 30 + self.particle.position * self.scale

        if y >= bottom_y:
            y = bottom_y
            self.running = False

        self.renderer.draw_ground()
        self.renderer.draw_particle(
            x=center_x,
            y=y,
            radius=self.particle.radius,
        )

        self.status_var.set(
            f'Время: {self.dt} с за шаг\n'
            f'Положение: {self.particle.position} м\n'
            f'Скорость: {self.particle.velocity} м/с\n'
            f'Сила сопротивления: '
            f'{self.particle.drag_force(self.viscosity)} Н'
        )

        if self.running:
            self.after_id = self.root.after(10, self._animate)

    def reset(self):
        """Остановить анимацию и очистить холст"""
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.renderer.clear()
        self.particle = None
        self.status_var.set('Задай параметры и нажми «Запустить»')

    def _close(self):
        """Закрыть приложение"""
        self.reset()
        self.root.destroy()
