"""Точка входа приложения"""

import tkinter as tk

from src.app import ResistanceApp


def main():
    """Запустить приложение"""
    root = tk.Tk()
    ResistanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
