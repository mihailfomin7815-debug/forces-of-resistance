"""Отрисовка симуляции на Tkinter Canvas"""


class ParticleRenderer:
    """Класс отрисовки"""
    def __init__(self, canvas):
        self.canvas = canvas

    def clear(self):
        self.canvas.delete('all')

    def draw_environment(self, boundary_y):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        self.canvas.create_rectangle(
            0, 0, width, boundary_y,
            fill='#000000',
            outline='',
            tags='environment',
        )

        self.canvas.create_rectangle(
            0, boundary_y, width, height,
            fill='#6e6e6e',
            outline='',
            tags='environment',
        )

    def draw_particle(self, x, y, radius):
        """Отрисовка частицы"""
        r = max(3, min(20, radius * 4000))

        self.canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill='',
            outline='#ffffff',
            width=2,
            tags='particle',
        )
