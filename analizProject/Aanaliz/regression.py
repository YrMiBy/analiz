# Модуль 'regression'
# Линейные корреляционный и регрессионный анализ
import math
from tkinter import *
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt
import select_2column
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = tk.Tk()  # окно
root.title("Линейная корреляция и регрессия")  # заголовок окна
exit_button = tk.Button(root, text="Выход", command=root.quit, font=('Arial', 14), background ='DarkSlateGray2')
exit_button.pack(side=tk.BOTTOM, pady=10)

def calculation_r():  # вычисление
    # вычисление параметров коэффициента корреляции
    global slope, intercept, r, p, std_err, text_result, rL, rU, column_1, column_2, name_x, name_y
    column_1 = df[name_column[0]]  # значения первого выбранного ряда из датафрейма
    column_2 = df[name_column[1]]  # значения второго выбранного ряда
    if column_1.count() == column_2.count() and column_1.count() > 3:
        n = column_1.count()
        name_x = name_column[0]  # имя первого ряда
        name_y = name_column[1]  # имя второго ряда
        slope, intercept, r, p, std_err = stats.linregress(column_1, column_2)  # расчет
        # slope-наклон, intercept-cдвиг, r-коэфф.корреляции, p-р-значение, std_err-стандартная ошибка
        if np.isnan(r) or np.isnan(p):  # Проверка получения значения nan
            label = Label(root, text=f'В рядах нет значений, или стандартное отклонение = 0')
            label.pack(anchor=NW, font=('Arial', 12), bg='yellow')
        else:
            if p < 0.05:
                text_result = 'значим'
                # Определение доверительного интервала для r
                try:
                    z = 0.5 * math.log((1 + r) / (1 - r))  # Это преобразование Фишера r в z
                    se = 1 / math.sqrt(n - 3)  # это стандартная ошибка для z-значения.
                    zl = z - se * 1.96  # границы интервала в z
                    zu = z + se * 1.96
                    rL = np.tanh(zl)  # границы интервала r
                    rU = np.tanh(zu)
                except:
                    label = Label(root, text=f'Ошибка определения доверительного интервала')
                    label.pack(anchor=NW)

                frame_root()
                open_file()
            else:
                text_result = 'не значим'
                label = Label(root, text=f'Коэффициент корреляции не значим')
                label.pack(anchor=NW)
    else:
        label = Label(root, text=f'В рядах разное количество значений или количество значений меньше 3')
        label.pack(anchor=NW)


def frame_root():  # Размещение графика и окна на экране
    # Создание фрейма для графика
    frame_graph = tk.Frame(root)  # фрейм для графика
    frame_graph.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Создание нового виджета для размещения окна с результатами
    frame_controls = tk.Frame(root)
    frame_controls.pack(side=tk.RIGHT, fill=tk.X)
    # Создание графика
    fig, ax = plt.subplots()
    column_2_hat = slope * column_1 + intercept  # Значение y в уравнении регрессии
    ax.scatter(column_1, column_2, color="green")  # точки диаграммы рассеяния
    ax.plot(column_1, column_2_hat, color="red")  # Линия регрессии
    ax.set_xlabel(name_x)
    ax.set_ylabel(name_y)
    ax.set_title(f'Диаграмма рассеяния')
    # Встраивание графика в tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # Размещение окна с данными
    result_text = f"""
            Ряд X: {name_x}, Ряд Y: {name_y}
            Коэффициент корреляции {text_result}
            Уровень значимости: 0,05
            Значение коэффициента корреляции: {round(r, 4)}
            95%-ный доверительный интервал для корреляционного отношения: {round(rL, 4), round(rU, 4)}
            Коэффициент детерминации: {round(r ** 2, 4)}
            P-значение: {round(p, 4)}
            Уравнение регрессии y = {round(slope, 4)} * x + {round(intercept, 4)} * y
            Стандартная ошибка: {round(std_err, 4)}
        """
    label = Label(frame_controls, text=result_text, justify=LEFT, font=('Arial', 14))
    label.pack(anchor=NW)


def open_file():  # Открываем (создаем) файл для записи
    file_name = "../../Analiz_dannych/file_result.txt"
    # `with` автоматически закрывает файл после работы с ним, даже если возникнет ошибка.
    with open(file_name, 'w', encoding="utf-8") as file:  # Открывает файл `file_result` в режиме записи ('w').
        # Записываем результаты в файл
        file.write(f'Сравниваемые ряды: {name_x} (х) и {name_y} (y)\n')
        file.write(f'Коэффициент корреляции {text_result}\n')
        file.write(f'Уровень значимости: 0,05\n')
        file.write(f'Значение коэффициента парной корреляции Пирсона: {round(r, 4)}\n')
        file.write(f'95%-ный доверительный интервал для коэффициента корреляции: '
            f'{[round(rL, 4), round(rU, 4)]}\n')
        file.write(f'Значение коэффициента детерминации: {round(r ** 2, 4)}\n')
        file.write(f'p-значение: {round(p, 4)}\n')
        file.write(f'Уравнение регрессии y = {round(slope, 4)} * x + {round(intercept, 4)}\n')
        file.write(f'Стандартная ошибка: {round(std_err, 4)}\n')


try:
    df = pd.read_csv('../../Analiz_dannych/data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)

name_column = select_2column.name_columns  # Выбор рядов в модуле 'select_2column'

clicks = 0
list_name_number = []  # список имен числовых рядов
list_name_number_clic = []  # список имен числовых рядов, выбранных для анализа
slope = 0
r = 0
p = 0
std_err = 0
text_result = ''
rL = 0
rU = 0
column_1 = ''
column_2 = ''
name_x = ''
name_y = ''

calculation_r()

root.mainloop()
