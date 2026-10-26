"""Общие фикстуры для тестов"""

import tkinter as tk

import pytest


@pytest.fixture
def tk_root():
    """Окно Tk для тестов виджетов"""
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip('Нет доступного дисплея для тестов Tkinter')

    root.geometry('+2000+2000')
    root.update()

    yield root

    try:
        root.destroy()
    except tk.TclError:
        pass
