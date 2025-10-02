import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры
num_molecules_solid = 25*25  # 12x12 для плотной решетки
num_molecules_liquid = 500  # Для жидкости
num_molecules_gas = 50  # Для газа

space_size = 10  # Размер области

vibration_amplitude = 0.005  # Амплитуда для твердого
liquid_speed = 0.15  # Скорость для жидкости
gas_speed = 1  # Скорость для газа

frames = 400  # Кадры
interval = 20  # Интервал
molecule_size = 20  # Размер точек

# Центр графика
center_x = space_size / 2
center_y = space_size / 2

# Твердое тело: центрированная решетка, заполняющая от 0 до space_size
grid_size = int(np.sqrt(num_molecules_solid))  # 12
offsets = np.linspace(-space_size / 2, space_size / 2, grid_size)
solid_x = center_x + np.repeat(offsets, grid_size)
solid_y = center_y + np.tile(offsets, grid_size)

# Жидкость: нормальное распределение вокруг центра, с clip для границ
sigma = space_size / 4  # Чтобы доходило до краев
liquid_x = np.clip(np.random.normal(center_x, sigma, num_molecules_liquid), 0, space_size)
liquid_y = np.clip(np.random.normal(center_y, sigma, num_molecules_liquid), 0, space_size)

# Газ: без изменений, в большей области
gas_x = np.random.uniform(0, space_size * 1.5, num_molecules_gas)
gas_y = np.random.uniform(0, space_size * 1.5, num_molecules_gas)

# Фигура с подграфиками
fig, (ax_solid, ax_liquid, ax_gas) = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Молекул в разных состояниях')

# Настройка осей: разные лимиты для уровнивания
ax_solid.set_xlim(0, space_size)
ax_solid.set_ylim(0, space_size)
ax_liquid.set_xlim(0, space_size)
ax_liquid.set_ylim(0, space_size)
ax_gas.set_xlim(0, space_size * 1.5)
ax_gas.set_ylim(0, space_size * 1.5)

for ax in [ax_solid, ax_liquid, ax_gas]:
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

ax_solid.set_title('Твердое тело')
ax_liquid.set_title('Жидкость')
ax_gas.set_title('Газ')

# Scatter
color = 'blue'
solid_scatter = ax_solid.scatter(solid_x, solid_y, color=color, s=molecule_size)
liquid_scatter = ax_liquid.scatter(liquid_x, liquid_y, color=color, s=molecule_size)
gas_scatter = ax_gas.scatter(gas_x, gas_y, color=color, s=molecule_size)

# Скорости для сглаживания
liquid_vx = np.random.normal(0, liquid_speed, num_molecules_liquid)
liquid_vy = np.random.normal(0, liquid_speed, num_molecules_liquid)
gas_vx = np.random.normal(0, gas_speed, num_molecules_gas)
gas_vy = np.random.normal(0, gas_speed, num_molecules_gas)


# Обновление
def update(frame):
    # Твердое тело: колебания
    solid_dx = np.random.normal(0, vibration_amplitude, num_molecules_solid)
    solid_dy = np.random.normal(0, vibration_amplitude, num_molecules_solid)
    solid_offsets = np.column_stack((solid_x + solid_dx, solid_y + solid_dy))

    # Жидкость: движение с clip для границ
    global liquid_x, liquid_y, liquid_vx, liquid_vy
    liquid_vx += np.random.normal(0, liquid_speed * 0.1, num_molecules_liquid)
    liquid_vy += np.random.normal(0, liquid_speed * 0.1, num_molecules_liquid)
    liquid_vx *= 0.9
    liquid_vy *= 0.9
    liquid_x = np.clip(liquid_x + liquid_vx, 0, space_size)
    liquid_y = np.clip(liquid_y + liquid_vy, 0, space_size)
    liquid_offsets = np.column_stack((liquid_x, liquid_y))

    # Газ: без изменений
    global gas_x, gas_y, gas_vx, gas_vy
    gas_vx += np.random.normal(0, gas_speed * 0.1, num_molecules_gas)
    gas_vy += np.random.normal(0, gas_speed * 0.1, num_molecules_gas)
    gas_vx *= 0.9
    gas_vy *= 0.9
    gas_x = (gas_x + gas_vx) % (space_size * 1.5)
    gas_y = (gas_y + gas_vy) % (space_size * 1.5)
    gas_offsets = np.column_stack((gas_x, gas_y))

    solid_scatter.set_offsets(solid_offsets)
    liquid_scatter.set_offsets(liquid_offsets)
    gas_scatter.set_offsets(gas_offsets)

    return solid_scatter, liquid_scatter, gas_scatter


ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=True)

plt.show()