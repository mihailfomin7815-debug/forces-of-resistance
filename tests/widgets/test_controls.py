"""Тесты панели управления (controls.py)"""

import tkinter as tk

from src.widgets.controls import SimulationControls


class TestSimulationControls:
    def test_creates_frame(self, tk_root):
        controls = SimulationControls(
            tk_root, on_start=lambda: None, on_reset=lambda: None,
        )

        assert isinstance(controls.frame, tk.Frame)

    def test_creates_start_and_reset_buttons(self, tk_root):
        controls = SimulationControls(
            tk_root, on_start=lambda: None, on_reset=lambda: None,
        )

        assert isinstance(controls.start_button, tk.Button)
        assert isinstance(controls.reset_button, tk.Button)
        assert controls.start_button.cget('text') == 'Старт'
        assert controls.reset_button.cget('text') == 'Сброс (R)'

    def test_start_button_calls_callback(self, tk_root):
        calls = []
        controls = SimulationControls(
            tk_root,
            on_start=lambda: calls.append('start'),
            on_reset=lambda: None,
        )

        controls.start_button.invoke()

        assert calls == ['start']

    def test_reset_button_calls_callback(self, tk_root):
        calls = []
        controls = SimulationControls(
            tk_root,
            on_start=lambda: None,
            on_reset=lambda: calls.append('reset'),
        )

        controls.reset_button.invoke()

        assert calls == ['reset']

    def test_hint_label_mentions_shortcuts(self, tk_root):
        controls = SimulationControls(
            tk_root, on_start=lambda: None, on_reset=lambda: None,
        )

        text = controls.hint_label.cget('text')

        assert 'R' in text
        assert 'Esc' in text

    
    def test_resistance_scale_exists(self, tk_root):
        controls = SimulationControls(
            tk_root,
            on_start=lambda: None,
            on_reset=lambda: None,
        )

        assert isinstance(controls.resistance_scale, tk.Scale)
        assert float(controls.resistance_scale.get()) == 100.0

    def test_resistance_scale_updates_label(self, tk_root):
        controls = SimulationControls(
            tk_root,
            on_start=lambda: None,
            on_reset=lambda: None,
        )

        controls.resistance_scale.set(150)

        assert controls.resistance_label.cget("text") == (
            "Сопротивление: 150%"
        )

    def test_resistance_scale_calls_callback(self, tk_root):
        values = []

        controls = SimulationControls(
            tk_root,
            on_start=lambda: None,
            on_reset=lambda: None,
            on_resistance_change=values.append,
        )

        controls.resistance_scale.set(50)

        assert values[-1] == 50
