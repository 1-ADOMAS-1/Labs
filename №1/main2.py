import numpy as np                               # для математических операций
from scipy.integrate import odeint               # odeint из scipy.integrate для решений дифференциальных

import matplotlib.pyplot as plt                  # для графиков
from matplotlib.animation import FuncAnimation   # для анимаций
from matplotlib.patches import Circle            # для объектов
import matplotlib.gridspec as gridspec           # для сложных сеток подграфиков


# переменные для экспириментов
# Цвета (в шестнадцатеричном (HEX) код)
earth_color = '#24c229'  # Зелёный для Земли
moon_color = '#b8b8b8'  # Серый для Луны

# переменные
l = 1.0     # длина маятника (м)
total = 10 # количество колебаний
theta0 = np.deg2rad(20)  # начальный угол (рад), увеличен для более заметных колебаний

# Параметры
g_earth = 9.81  # ускорение свободного падения на Земле (м/с²)
g_moon = 1.62  # на Луне (м/с²)
interval = 50 # Миллисекуны = 1секунде * 10^(-3)
FPS = 1000/interval # кадры в секунды = секунда /

# количество кадров
T = 2*np.pi*np.sqrt(l/g_earth)*total
frames = int(T*FPS) # количество кадров

t = np.linspace(0, T, frames)
# с 0 до T в количестве frames элементов

# Уравнения движения маятника дифференциальное уравнение
def pend(y, t, g, l, b):
    theta, omega = y # угол - насколько маятник откланен, скорость изменение угла
    return [omega, -(g / l) * theta - b*omega]
# функция pend система ОДУ где:
# y - вектор состояния (угол и угловая скорость)
# t - время, g и l - Параметры
b = 0.1
# Решение для Земли и Луны
y_earth = odeint(pend, [theta0, 0], t, args=(g_earth, l, b))
y_moon =  odeint(pend, [theta0, 0], t, args=(g_moon, l, b))
# Создание фигуры и сетки
# основная фигура 12X8 дюймов
fig = plt.figure(figsize=(12, 8))
gs = gridspec.GridSpec(2, 2) # сетка 2X2 для подграфиков

ax_phase = fig.add_subplot(gs[0, 0])  # Сверху слева: эллипс (фазовый портрет)
ax_time = fig.add_subplot(gs[1, 0])   # Снизу слева: диаграмма θ(t)
ax_earth = fig.add_subplot(gs[0, 1])  # Справа сверху: маятник на Земле
ax_moon = fig.add_subplot(gs[1, 1])   # Справа снизу: маятник на Луне

# Настройка осей для маятников
margin = 0.3 + T/50*1.1# запас
for ax in [ax_earth, ax_moon]:
    # устанавливаем область анимации
    ax.set_xlim(-(l+margin), l+margin)
    ax.set_ylim(-(l+margin), margin)
    ax.set_aspect('equal') # делает масштаб по x и y одинаковым
    ax.grid(True) # включает сетку

# заголовки
ax_earth.set_title('Маятник на Земле')
ax_moon.set_title('Маятник на Луне')

# Диаграмма времени (снизу слева)
# рисуем график луны и земли угол(t)
ax_time.plot(t, y_earth[:, 0], color=earth_color, alpha=0.3, label='Земля')
ax_time.plot(t, y_moon[:, 0], color=moon_color, alpha=0.3, label='Луна')
ax_time.set_xlabel('Время (с)')
ax_time.set_ylabel('Угол (рад)')
ax_time.legend() # из label
ax_time.grid(True)

# Фазовый портрет (эллипсы, сверху слева)
ax_phase.plot(y_earth[:, 0], y_earth[:, 1], color=earth_color, alpha=0.3, label='Земля')
ax_phase.plot(y_moon[:, 0], y_moon[:, 1], color=moon_color, alpha=0.3, label='Луна')
ax_phase.set_xlabel('Угол (θ)')
ax_phase.set_ylabel('Угловая скорость (ω)')
ax_phase.set_title('Фазовый портрет (эллипсы)')
ax_phase.legend()
ax_phase.grid(True)

# Элементы анимации
# *_bob: круги в координатах xy и радиус, fc-задает цвет
# *_line: линии 'o-' с кругом на конце, lw толщина, [], [] в пустые массивы будут добавляться данные позже
# ax_*.add_patch(*_bob) добавляем круги на подграфики маятников
earth_line, = ax_earth.plot([], [], 'o-', lw=2, color=earth_color)
earth_bob = Circle((0, 0), 0.08, fc=earth_color)
ax_earth.add_patch(earth_bob)

moon_line, = ax_moon.plot([], [], 'o-', lw=2, color=moon_color)
moon_bob = Circle((0, 0), 0.08, fc=moon_color)
ax_moon.add_patch(moon_bob)

# тоже самое
time_earth_line, = ax_time.plot([], [], color=earth_color, lw=2)
time_earth_point, = ax_time.plot([], [], 'o',color=earth_color, ms=8)

time_moon_line, = ax_time.plot([], [], color=moon_color, lw=2)
time_moon_point, = ax_time.plot([], [], 'o',color=moon_color, ms=8)

phase_earth_point, = ax_phase.plot([], [], 'o',color=earth_color, ms=8)
phase_moon_point, = ax_phase.plot([], [], 'o',color=moon_color, ms=8)


# Инициализация анимации
def init():
    earth_line.set_data([], [])
    earth_bob.center = (0, 0)
    moon_line.set_data([], [])
    moon_bob.center = (0, 0)
    time_earth_line.set_data([], [])
    time_earth_point.set_data([], [])
    time_moon_line.set_data([], [])
    time_moon_point.set_data([], [])
    phase_earth_point.set_data([], [])
    phase_moon_point.set_data([], [])
    return (earth_line, earth_bob, moon_line, moon_bob, time_earth_line, time_earth_point,
            time_moon_line, time_moon_point, phase_earth_point, phase_moon_point)


# Обновление кадров
def update(frame):
    # Маятник на Земле
    x_earth = l * np.sin(y_earth[frame, 0])
    y_earth_pos = -l * np.cos(y_earth[frame, 0])

    earth_line.set_data([0, x_earth], [0, y_earth_pos])
    earth_bob.center = (x_earth, y_earth_pos)

    # Маятник на Луне
    x_moon = l * np.sin(y_moon[frame, 0])
    y_moon_pos = -l * np.cos(y_moon[frame, 0])
    moon_line.set_data([0, x_moon], [0, y_moon_pos])
    moon_bob.center = (x_moon, y_moon_pos)

    # Диаграмма времени
    time_earth_line.set_data(t[:frame + 1], y_earth[:frame + 1, 0])
    time_earth_point.set_data([t[frame]], [y_earth[frame, 0]])
    time_moon_line.set_data(t[:frame + 1], y_moon[:frame + 1, 0])
    time_moon_point.set_data([t[frame]], [y_moon[frame, 0]])

    # Фазовый портрет (точки)
    phase_earth_point.set_data([y_earth[frame, 0]], [y_earth[frame, 1]])
    phase_moon_point.set_data([y_moon[frame, 0]], [y_moon[frame, 1]])

    return (earth_line, earth_bob, moon_line, moon_bob, time_earth_line, time_earth_point,
        time_moon_line, time_moon_point, phase_earth_point, phase_moon_point)

# Создание анимации
anim = FuncAnimation(fig, update, frames=frames, init_func=init, blit=True, interval=interval)
# fig:           основная фигура на которой находятся все 4 графика
# update:        функция которую будут использовать
# frames=frames: количество кадров - frames = int(T*time)
# init_func:     функция Инициализация анимации
# blit
# interval: в миллисекунда (0.001с = 1мс)

# Для сохранения в GIF
# anim.save('pendulum_animation.gif', writer='pillow', fps=30)

plt.tight_layout()
plt.show()
