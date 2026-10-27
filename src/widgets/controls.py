
"""Панель управления симуляцией"""

import tkinter as tk


class SimulationControls:
    """Панель кнопок и настройки силы сопротивления"""

    def __init__(
        self,
        root,
        on_start,
        on_reset,
        on_resistance_change=None,
    ):
        self.root = root
        self.on_start = on_start
        self.on_reset = on_reset
        self.on_resistance_change = (
            on_resistance_change or (lambda value: None)
        )

        self.frame = tk.Frame(
            root,
            background='#1a1a1a',
        )
        self.frame.pack(
            side=tk.BOTTOM,
            fill=tk.X,
        )

        self._create_widgets()

    def _create_widgets(self):
        button_style = {
            'background': '#2a2a2a',
            'foreground': '#ffffff',
            'activebackground': '#3a3a3a',
            'activeforeground': '#ffffff',
            'relief': tk.FLAT,
            'borderwidth': 0,
            'padx': 16,
            'pady': 6,
            'font': ('Segoe UI', 10),
            'cursor': 'hand2',
        }

        self.start_button = tk.Button(
            self.frame,
            text='Старт',
            command=self.on_start,
            **button_style,
        )
        self.start_button.pack(
            side=tk.LEFT,
            padx=8,
            pady=8,
        )

        self.reset_button = tk.Button(
            self.frame,
            text='Сброс (R)',
            command=self.on_reset,
            **button_style,
        )
        self.reset_button.pack(
            side=tk.LEFT,
            padx=8,
            pady=8,
        )

        self.resistance_label = tk.Label(
            self.frame,
            text='Сопротивление: 100%',
            background='#1a1a1a',
            foreground='#ffffff',
            font=('Segoe UI', 9),
        )
        self.resistance_label.pack(
            side=tk.LEFT,
            padx=(8, 2),
            pady=8,
        )

        self.resistance_var = tk.IntVar(value=100)

        self.resistance_scale = tk.Scale(
            self.frame,
            from_=0,
            to=200,
            resolution=10,
            orient=tk.HORIZONTAL,
            length=130,
            showvalue=False,
            variable=self.resistance_var,
            background='#1a1a1a',
            foreground='#ffffff',
            troughcolor='#3a3a3a',
            highlightthickness=0,
            activebackground='#777777',
        )
        self.resistance_scale.pack(
            side=tk.LEFT,
            padx=4,
            pady=4,
        )

        self.resistance_var.trace_add(
            'write',
            self._on_resistance_var_change,
        )

        self._update_resistance(
            self.resistance_var.get()
        )

        self.hint_label = tk.Label(
            self.frame,
            text='R — перезапуск  Esc — выход',
            background='#1a1a1a',
            foreground='#888888',
            font=('Segoe UI', 9),
        )
        self.hint_label.pack(
            side=tk.RIGHT,
            padx=12,
        )

    def _on_resistance_var_change(self, *_):
        """Обрабатывает изменение значения шкалы"""
        self._update_resistance(
            self.resistance_var.get()
        )

    def _update_resistance(self, value):
        """Обновляет подпись и передаёт значение в приложение"""
        percent = int(float(value))

        self.resistance_label.config(
            text=f'Сопротивление: {percent}%'
        )

        self.on_resistance_change(percent)
