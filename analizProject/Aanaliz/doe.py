# Модуль 'doe'
# Анализируется полный факторный двухуровневый (-1, 1) эксперимент
# Задача - нахождение функции отклика
import itertools
import math
import tkinter as ttk
from tkinter import *
import numpy as np
import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
from scipy.stats import bartlett


def center_window():  # Центрирование окна на экране
    root.update_idletasks()  # Обновление интерфейса
    width = root.winfo_width()  # Ширина окна
    height = root.winfo_height()
    screen_width = root.winfo_screenwidth()  # ширина экрана
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2  # координата левой верхней точки окна
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")  # Размещение окна


def open_file():  # Открываем (создаем) файл для записи
    file_name = "../../Analiz_dannych/file_result.txt"
    # `with` автоматически закрывает файл после работы с ним, даже если возникнет ошибка.
    with open(file_name, 'w', encoding="utf-8") as file:  # Открывает файл `file_result` в режиме записи ('w').
        # Записываем результаты в файл
        file.write(f'Уровень значимости: 0,05\n')
        file.write(f'Дисперсии опытов однородны\n')
        file.write(f'Дисперсия воспроизводимости: {round(std_y, 4)}\n')
        # file.write(f'Коэффициенты регрессии (если значение коэффициента равно 0, он не значим):\n')
        for key, value in dict_file.items():
            text_i = f'Коэффициент регрессии {key} = {value}\n'
            file.write(text_i)
        file.write(f'Значимые коэффициенты регрессии:\n')
        for element in list_file:
            text_i = f'Коэффициент регрессии {element}\n'
            file.write(text_i)
        if f_op < f_cr:
            file.write(f'Модель адекватна на уровне 95%\n')
        else:
            file.write(f'Модель не адекватна на уровне 95%\n')


# Создание окна
root = ttk.Tk()  # Главное окно
root.title("Планирование эксперимента")  # заголовок окна
root.wm_minsize(400, 400)
root.config(padx=10, pady=10)
center_window()  # функция центрирования окна

# Используемые переменные
num_levels = 2  # Количество уровней
factors = 0  # Количество факторов
num_column = 0  # Количество столбцов в файле df (повторных опытов)
num_string = 0  # Количество строк с данными (экспериментов) в файле df
alpha = 0.05  # Уровень значимости
flag = 0

try:
    df = pd.read_csv('../../Analiz_dannych/data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)


def checks():  # Проверки
    global num_string, num_column, factors
    # Определение количества столбцов во фрейме (повторных опытов)
    try:
        num_column = len(df.loc[0])
    except KeyError as e:
        label = Label(root, text=f'Ошибка в исходном файле: {e}')
        label.pack(anchor=NW)
    else:
        # Проверка количества параллельных опытов
        if num_column < 2:
            label = Label(root, text='Число параллельных опытов должно быть не меньше 2')
            label.pack(anchor=NW)
        else:
            # Проверка на наличие NaN и 0
            if df.isna().any().any() == True or (df == 0).any().any() == True:
                label = Label(root, text='Ошибка в исходном файле')
                label.pack(anchor=NW)
            else:
                # Проверка соответствия количества факторов количеству экспериментов
                num_string = int(len(df.index))  # Количество строк
                factors = math.log2(int(num_string))  # Количество факторов
                if factors.is_integer():  # Проверка, является ли результат целым числом
                    factors = int(factors)
                    calculations()
                else:
                    label = Label(root, text='Количество факторов не соответствует количеству экспериментов')
                    label.pack(anchor=NW)


def calculations():
    global std_y, dict_file, list_file, f_op, f_cr, factors, flag, coef_sn
    # Генерируем комбинации уровней для факторов
    levels = [-1, 1]  # Уровни -1 и 1
    combinations = list(itertools.product(levels, repeat=int(factors)))  # Список комбинаций
    # Создаем вспомогательный DataFrame для расчета
    new_df = pd.DataFrame(combinations, columns=[f'Фактор {i + 1}' for i in range(int(factors))])

    # Добавляем взаимодействия факторов.
    for i in range(int(factors)):
        for j in range(i + 1, int(factors)):
            interaction_name = f'Взаимодействие {i + 1}*{j + 1}'
            new_df[interaction_name] = new_df[f'Фактор {i + 1}'] * new_df[f'Фактор {j + 1}']

    # Определяем параметры отклика.
    result_mean = df.mean(axis=1)  # среднее (перечень)
    list_std = []  # Инициализация списка для хранения значений
    result_std = df.var(axis=1)  # выборочная дисперсия (перечень)

    # Проверка однородности дисперсий между строками с помощью теста Кохрана (Бартлетта)
    groups = []  # список, в который добавляете значения каждой строки
    # Цикл перебора фрейма по индексу index.
    for index in range(len(df)):
        groups.append(df.iloc[index].values)
        if np.var(groups) == 0:  # Проверка значения дисперсии экспериментов
            label = Label(root, text=f'Дисперсия равна 0 для эксперимента {index+1}')
            label.pack(anchor=NW)
            flag = 1
            break
    if flag != 1:
        statistic, p_value = bartlett(*groups)  # Тест Кохрана (Бартлетта)
        if p_value < 0.05:
            label = Label(root, text='Дисперсии опытов неоднородны, анализ применять нельзя')
            label.pack(anchor=NW)
        else:
            label = Label(root, text='Дисперсии опытов однородны')
            label.pack(anchor=NW)

            # Определяем дисперсию параметра (дисперсию воспроизводимости)
            std_y = (result_std.sum(axis=0)) / num_string
            text_i = f'Дисперсия воспроизводимости: {round(std_y, 4)}'
            label = Label(root, text=text_i)
            label.pack(anchor=NW)

            # Определяем стандартное отклонение коэффициентов регрессии
            std_b = math.sqrt(std_y / (num_string * num_column))

            # Вводится столбец фиктивной переменной (все +1) для оценки свободного члена b0
            new_df = sm.add_constant(new_df)

            # Подгонка модели
            model = sm.OLS(result_mean, new_df).fit()

            # Получение коэффициентов (методом наименьших квадратов)
            dict_file = {}  # Создаем словарь для использования в функции 'open_file'
            coefficients = model.params  # перечень коэффициентов (фрейм series)
            series = pd.Series(coefficients)  # Перечень коэффициентов в виде объекта series
            for index, value in series.items():  # Вывод значений коэффициентов
                text_i = f'Коэффициент фактора: {index}, равен: {round(value, 4)}'
                label = Label(root, text=text_i)
                label.pack(anchor=NW)
                dict_file[index] = round(value, 4)  # Заполняем словарь

            # Проверка значимости коэффициентов регрессии
            list_file = []  # Создаем список для использования в функции 'open_file'
            fd = num_string * (num_column - 1)  # Число степеней свободы
            try:
                t_statistics = abs(stats.t.ppf(alpha / 2, fd))  # критическое (табличное) значение критерия Стьюдента.
            except ZeroDivisionError:
                label = Label(root, text='Число степеней свободы при оценке значимости коэффициентов равно 0')
                label.pack(anchor=NW)
            else:
                coef_sn = 0  # Число значимых коэффициентов регрессии
                for i in range(len(coefficients)):  # Проверка значимости коэффициентов
                    if abs(coefficients.iloc[i]) >= (t_statistics * std_b):
                        text_i = f'Коэффициент {round(coefficients, 4).iloc[i]} значим на уровне {alpha}'
                        label = Label(root, text=text_i)
                        label.pack(anchor=NW)  # Прорисовка текстовой метки - расположение слева, вверху
                        coef_sn = coef_sn + 1
                        list_file.append(round(coefficients, 4).iloc[i])  # Заполняем список
                    else:
                        text_i = f'Коэффициент {round(coefficients, 4).iloc[i]} не значим на уровне {alpha}'
                        label = Label(root, text=text_i)
                        label.pack(anchor=NW)
                        coefficients.iloc[i] = 0  # незначимый коэффициент = 0
            # Определение дисперсии адекватности модели.
            std_ad = new_df  # Создаем фрейм для расчета дисперсии адекватности модели
            # Добавление значений коэффициентов в виде новой строки
            std_ad = pd.concat([std_ad, coefficients.to_frame().T], ignore_index=True)
            # Определяем значение отклика, вычисленного по уравнению регрессии
            y_list = []  # Инициализация списка для хранения значений y_list
            for i in range(len(std_ad.index) - 1):
                y_i = (std_ad.iloc[i] * std_ad.iloc[-1]).sum(axis=0)  # значения по уравнению
                y_list.append(y_i)  # Сохраняем значения в список.
            # Преобразуем в Series.
            x1_series = pd.Series(y_list)  # Это, чтобы использовать в дальнейших расчетах
            try:
                fd = (num_string - coef_sn + 1)  # Число степеней свободы
            except ZeroDivisionError:
                label = Label(root, text='Число степеней свободы при определении дисперсии адекватности модели равно 0')
                label.pack(anchor=NW)
            else:
                std_ad = ((df.mean(axis=1) - x1_series) ** 2).sum(axis=0) * num_column / fd  # дисперсия адекватности
                text_i = f'Дисперсия адекватности: {round(std_ad, 5)}'
                label = Label(root, text=text_i)
                label.pack(anchor=NW)

                # Проверка адекватности модели по критерию Фишера
                f_op = std_ad / std_y  # Эмпирическое значение критерия адекватности
                dfn = num_string - coef_sn  # Число степеней свободы числителя
                dfd = num_string * (num_column - 1)  # Число степеней свободы знаменателя
                f_cr = stats.f.ppf((1 - alpha), dfn, dfd)  # Табличное значение критерия Фишера
                if f_op < f_cr:
                    label = Label(root, text='Модель адекватна на уровне 95%')
                    label.pack(anchor=NW)
                    open_file()
                else:
                    label = Label(root, text='Модель неадекватна на уровне 95%')
                    label.pack(anchor=NW)


checks()

root.mainloop()
