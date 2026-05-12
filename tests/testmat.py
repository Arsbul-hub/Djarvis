import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# 1. Подготовка основы
fig, ax = plt.subplots()
x_data = np.linspace(0, 2*np.pi, 100)
line, = ax.plot([], [])  # Создаем пустую линию

# Настраиваем границы осей
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1.5, 1.5)

# 2. Функция обновления для каждого кадра
def update(frame):
    # Генерируем новые данные Y на основе номера кадра
    y_data = np.sin(x_data + frame / 10.0)
    line.set_data(x_data, y_data)  # Обновляем данные линии
    return line,

# 3. Создание и запуск анимации
ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)

plt.show()
