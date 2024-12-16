# Модуль podgonka_ks
# Подгонка распределения ряда с использованием теста Колмогорова-Смирнова

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import select_1column

try:
    df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)

name_column = select_1column.name_column   # Выбор ряда в модуле 'select_1column'

data = np.asarray(df[name_column], dtype=float)

# Распределения для проверки
distributions = ['norm', 'expon', 'uniform',  'laplace', 'triang']

# Словарь для хранения p-values
p_values = {}


# Функция для проверки соответствия
def check_fit(data, distributions):
    results = {}
    for distribution in distributions:
        dist = getattr(stats, distribution)
        # Оценка параметров распределения
        params = dist.fit(data)

        # Выполнение теста Колмогорова-Смирнова
        D, p_value = stats.kstest(data, distribution, args=params)
        # Сохранение p-value в словарь
        p_values[distribution] = p_value
        results[distribution] = (D, p_value, params)

    return results

# Проверка соответствия
fit_results = check_fit(data, distributions)

# Нахождение максимального p-value и соответствующего распределения
max_distribution = max(p_values, key=p_values.get)
max_p_value = p_values[max_distribution]
#print(f'Максимальное значение p-value: {max_p_value} для распределения {max_distribution}')

# Визуализация результатов
plt.figure(figsize=(12, 8))

# Гистограмма данных
plt.hist(data, bins=20, density=True, alpha=0.5, color='gray', label='Data')

x = np.linspace(min(data), max(data), 100)

for dist, (D, p, params) in fit_results.items():
    # Получаем теоретическую кривую распределения
    pdf = getattr(stats, dist).pdf(x, *params)
    plt.plot(x, pdf, label=f'{dist} (D={D:.4f}, p={p:.4f})')

plt.title('Сравнение данных с теоретическими распределениями')
plt.xlabel('Значение')
plt.ylabel('Плотность вероятности')
plt.legend()
plt.grid()
plt.show()
