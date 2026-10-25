"""Панель управления симуляцией"""

import tkinter as tk


class SimulationControls:
    """Нижняя панель с кнопками управления анимацией"""

    def __init__(self, root, on_start, on_reset):
        self.root = root
        self.on_start = on_start
        self.on_reset = on_reset

        self.frame = tk.Frame(root, background='#1a1a1a')
        self.frame.pack(side=tk.BOTTOM, fill=tk.X)

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
        self.start_button.pack(side=tk.LEFT, padx=8, pady=8)

        self.reset_button = tk.Button(
            self.frame,
            text='Сброс (R)',
            command=self.on_reset,
            **button_style,
        )
        self.reset_button.pack(side=tk.LEFT, padx=8, pady=8)

        self.hint_label = tk.Label(
            self.frame,
            text='R — перезапуск      Esc — выход',
            background='#1a1a1a',
            foreground='#888888',
            font=('Segoe UI', 9),
        )
        self.hint_label.pack(side=tk.RIGHT, padx=12)
