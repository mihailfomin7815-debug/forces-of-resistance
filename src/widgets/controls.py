
"""Виджеты управления симуляцией"""

import tkinter as tk
from tkinter import ttk


class SimulationControls:
    """Панель ввода параметров и управления симуляцией"""

    def __init__(self, parent, on_start, on_reset):
        """Создать панель и подключить обработчики кнопок"""
        self.frame = ttk.Frame(parent, padding=10)
        self.frame.pack(side=tk.RIGHT, fill=tk.Y)

        ttk.Label(
            self.frame,
            text='Силы сопротивления',
            font=('Arial', 14, 'bold'),
        ).pack(pady=(0, 12))

        self.radius_var = tk.DoubleVar(value=0.001)
        self.mass_var = tk.DoubleVar(value=0.01)
        self.velocity_var = tk.DoubleVar(value=0.0)
        self.viscosity_var = tk.DoubleVar(value=0.001)

        self._add_field('Радиус частицы (м)', self.radius_var)
        self._add_field('Масса частицы (кг)', self.mass_var)
        self._add_field('Начальная скорость (м/с)', self.velocity_var)
        self._add_field('Вязкость среды (Па·с)', self.viscosity_var)

        ttk.Button(
            self.frame,
            text='Запустить',
            command=on_start,
        ).pack(fill=tk.X, pady=(12, 4))

        ttk.Button(
            self.frame,
            text='Сбросить',
            command=on_reset,
        ).pack(fill=tk.X, pady=4)

        self.status_var = tk.StringVar(
            value='Задай параметры и нажми «Запустить»'
        )
        ttk.Label(
            self.frame,
            textvariable=self.status_var,
            wraplength=210,
        ).pack(pady=10)

    def _add_field(self, label, variable):
        """Добавить подпись и поле ввода"""
        ttk.Label(self.frame, text=label).pack(anchor='w')
        ttk.Entry(
            self.frame,
            textvariable=variable,
        ).pack(fill=tk.X, pady=(0, 8))
