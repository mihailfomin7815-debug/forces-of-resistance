"""Отрисовка частиц на холсте Tkinter"""


class ParticleRenderer:
    """Отвечает за визуальное представление частицы"""

    def __init__(self, canvas, scale=1000.0):
        """Сохранить холст и масштаб отображения"""
        self.canvas = canvas
        self.scale = scale

    def clear(self):
        """Очистить область рисования"""
        self.canvas.delete('all')

    def draw_particle(self, x, y, radius):
        """Нарисовать частицу по координатам холста"""
        display_radius = max(4, min(25, radius * self.scale))

        self.canvas.create_oval(
            x - display_radius,
            y - display_radius,
            x + display_radius,
            y + display_radius,
            fill='#4a90e2',
            outline='#245580',
        )

    def draw_ground(self):
        """Нарисовать нижнюю границу области движения"""
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        ground_y = height - 30

        self.canvas.create_line(
            0,
            ground_y,
            width,
            ground_y,
            fill='#aaaaaa',
        )
