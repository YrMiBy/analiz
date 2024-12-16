# Подгонка  распределений, имеющихся в scipy
import pandas as pd
from scipy import stats
import select_1column
import numpy as np
import warnings
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt

try:
    df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)
name_column = select_1column.name_column   #Выбор ряда в модуле 'select_1column'

data = np.asarray(df[name_column], dtype=float)

# Рассматриваемые эмпирические данные
sse = {}  # Словарь для хранения сумм квадратичных ошибок

for dist_name in dir(stats):
    distribution = getattr(stats, dist_name)
    # Проверка, является ли объект распределением и имеет ли он метод fit
    if isinstance(distribution, stats.rv_continuous) and hasattr(distribution, 'fit'):
        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')

            try:
                # Подгонка распределения и расчёт суммы квадратных ошибок
                params = distribution.fit(data)
                fitted_pdf = distribution.pdf(np.sort(data), *params[:-2], loc=params[-2], scale=params[-1])
                sse[dist_name] = np.sum(np.power(data-fitted_pdf, 2.0))
            except Exception as e:
                print(f"Ошибка при подгонке для {dist_name}: {e}")

# Выбор распределения, наилучшим образом описывающего данные
if sse:
    stats_fit = min(sse, key=sse.get)
    print(f"Наилучшее распределение: {stats_fit}")
else:
    print("Не удалось подогнать ни одно распределение.")
