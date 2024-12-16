# Модуль correl_relation. Определение корреляционного отношения
import tkinter as tk
import math
from tkinter import *
import numpy as np
import pandas as pd
import scipy.stats as stats
from matplotlib import pyplot as plt
import select_2column
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculation():  # Расчет
    global corr_ratio_XY, corr_ratio_YX, text_zn, rL, rU, X_name, Y_name, X, Y
    name_column = select_2column.name_columns  # Выбор рядов в модуле 'select_2column'

    X_name = name_column[0]  # имя первого ряда
    Y_name = name_column[1]
    X = np.array(df[X_name])  # значения 1 ряда
    Y = np.array(df[Y_name])

    try:
        # Для удобства работы сформируем отдельный DataFrame из двух переменных - X и Y:
        pd.DataFrame({'X': X, 'Y': Y})
        p_level = 0.95  # принятая вероятность
        n_X = len(X)  # Объем выборки
        n_Y = len(Y)
        matrix_XY_df = pd.DataFrame({'X': X, 'Y': Y})  # Переменная matrix_XY_df для работы с группированными данными

        # 1. Группировка исходных данных X и Y:
        # Определение числа интервалов по формуле Стерджесса; минимальное число интервалов 2:
        group_int_number = math.floor(3.322 * math.log(n_X, 10) + 1)
        if int(group_int_number) < 2:
            group_int_number = 2
        K_X = group_int_number
        K_Y = group_int_number
        # Группировка данных с помощью функции pandas.cut.
        # В результате получим новые признаки cut_X и cut_X, которые показывают, в какой из интервалов
        # попадает конкретное значение X и Y. Полученные новые признаки добавим в DataFrame matrix_XY_df:
        cut_X = pd.cut(X, bins=K_X)
        cut_Y = pd.cut(Y, bins=K_Y)
        matrix_XY_df['cut_X'] = cut_X
        matrix_XY_df['cut_Y'] = cut_Y
        # Получение корреляционной таблицы с помощью функции pandas.crosstab:
        CorrTable_df = pd.crosstab(
            index=matrix_XY_df['cut_X'],
            columns=matrix_XY_df['cut_Y'],
            rownames=['cut_X'],
            colnames=['cut_Y'])

        # 2. Расчет корреляционного отношения
        # Для дальнейших расчетов приведем корреляционную таблицу к типу numpy.ndarray:
        CorrTable_np = np.array(CorrTable_df)
        num_rows_x = CorrTable_np.shape[0]  # Определение количества строк в корреляционной таблице
        num_column_y = CorrTable_np.shape[1]  # Определение количества столбцов
        # Итоги корреляционной таблицы по строкам и столбцам:
        n_group_X = [np.sum(CorrTable_np[i]) for i in range(num_rows_x)]  # итоги по строкам
        n_group_Y = [np.sum(CorrTable_np[:, j]) for j in range(num_column_y)]  # итоги по столбцам
        # Среднегрупповые значения переменной X
        Xboun_mean = [(CorrTable_df.index[i].left + CorrTable_df.index[i].right) / 2 for i in range(num_rows_x)]
        Xboun_mean[0] = (np.min(X) + CorrTable_df.index[0].right) / 2  # исправляем значения в крайних интервалах
        Xboun_mean[num_rows_x - 1] = (CorrTable_df.index[num_rows_x - 1].left + np.max(X)) / 2
        # Среднегрупповые значения переменной Y
        Yboun_mean = [(CorrTable_df.columns[j].left + CorrTable_df.columns[j].right) / 2 for j in range(num_column_y)]
        Yboun_mean[0] = (np.min(Y) + CorrTable_df.columns[0].right) / 2  # исправляем значения в крайних интервалах
        Yboun_mean[num_column_y - 1] = (CorrTable_df.columns[num_column_y - 1].left + np.max(Y)) / 2
        # Средневзевешенные значения X и Y для каждой группы:
        Xmean_group = [np.sum(CorrTable_np[:, j] * Xboun_mean) / n_group_Y[j] for j in range(num_column_y)]
        Ymean_group = [np.sum(CorrTable_np[i] * Yboun_mean) / n_group_X[i] for i in range(num_rows_x)]
        # Общая дисперсия X и Y:
        Sum2_total_X = np.sum(n_group_X * (Xboun_mean - np.mean(X)) ** 2)
        Sum2_total_Y = np.sum(n_group_Y * (Yboun_mean - np.mean(Y)) ** 2)
        # Sum2_total_X = np.sum(n_group_X*(Xboun_mean - np.mean(X))**2)
        # Sum2_total_Y = np.sum(n_group_Y*(Yboun_mean - np.mean(Y))**2)
        # Межгрупповая дисперсия X и Y (дисперсия групповых средних):
        Sum2_between_group_X = np.sum(n_group_Y * (Xmean_group - np.mean(X)) ** 2)
        Sum2_between_group_Y = np.sum(n_group_X * (Ymean_group - np.mean(Y)) ** 2)
        # Эмпирическое корреляционное отношение:
        corr_ratio_XY = math.sqrt(Sum2_between_group_Y / Sum2_total_Y)
        corr_ratio_YX = math.sqrt(Sum2_between_group_X / Sum2_total_X)

        # 3. Проверка значимости корреляционного отношения:
        # расчетное значение статистики критерия Фишера
        F_corr_ratio_calc = (n_X - K_X) / (K_X - 1) * corr_ratio_XY ** 2 / (1 - corr_ratio_XY ** 2)
        # табличное значение статистики критерия Фишера.
        dfn = K_X - 1  # Число степеней свободы числителя
        dfd = n_X - K_X  # Число степеней свободы знаменателя
        # loc - смещение, добавляемое к результату, scale - параметр масштаба: умножается на результат
        F_corr_ratio_table = stats.f.ppf(p_level, dfn, dfd, loc=0, scale=1)
        a_corr_ratio_calc = 1 - stats.f.cdf(F_corr_ratio_calc, dfn, dfd, loc=0, scale=1)  # альфа
        # выводF_corr_ratio_table
        if F_corr_ratio_calc < F_corr_ratio_table:
            text_zn = 'не значимо'
            label = Label(root, text='Корреляционное отношение не значимо на уровне 95%')
            label.pack(anchor=NW)
        else:
            text_zn = 'значимо'

            # 4. Доверительный интервал для корреляционного отношения:
            # число степеней свободы
            f1 = round((K_X - 1 + n_X * corr_ratio_XY ** 2) ** 2 / (K_X - 1 + 2 * n_X * corr_ratio_XY ** 2))
            f2 = n_X - K_X
            # вспомогательные величины
            z1 = ((n_X - K_X) / n_X * corr_ratio_XY ** 2 / (1 - corr_ratio_XY ** 2) * 1 /
                  stats.f.ppf(0.95, f1, f2, loc=0, scale=1) - (K_X - 1) / n_X)
            z2 = ((n_X - K_X) / n_X * corr_ratio_XY ** 2 / (1 - corr_ratio_XY ** 2) * 1 /
                  stats.f.ppf(1 - 0.95, f1, f2, loc=0, scale=1) - (K_X - 1) / n_X)
            # доверительный интервал
            rL = math.sqrt(z1) if math.sqrt(z1) >= 0 else 0
            rU = math.sqrt(z2) if math.sqrt(z2) <= 1 else 1

            frame_root()
            open_file()
    except ZeroDivisionError:
        label = Label(root, text=f'Ошибка: деление на 0')
        label.pack(anchor=NW)
    except Exception as e:
        label = Label(root, text=f'Ошибка в вычислении: {e}')
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
    ax.scatter(X, Y, color="green")  # точки диаграммы рассеяния
    ax.set_xlabel(X_name)
    ax.set_ylabel(Y_name)
    ax.set_title(f'Диаграмма рассеяния')
    # Встраивание графика в tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    # Размещение окна с данными
    result_text = f"""
        Ряд X: {X_name}, Ряд Y: {Y_name}
        Корреляционное отношение: {text_zn}
        Уровень значимости: 0,05
        Значение корреляционного отношения XY: {round(corr_ratio_XY, 3)}
        Значение корреляционного отношения YX: {round(corr_ratio_YX, 3)}
        Значение 'η²' XY: {round(corr_ratio_XY ** 2, 3)}
        Значение 'η²' YX: {round(corr_ratio_YX ** 2, 3)}
        95%-ный доверительный интервал для корреляционного отношения XY: {[round(rL, 3), round(rU, 3)]}
        """
    label = Label(frame_controls, text=result_text, justify=LEFT, font=('Arial', 14))
    label.pack(anchor=NW)

def open_file():  # Файл с результатами анализа
    file_name = "file_result.txt"
    # `with` автоматически закрывает файл после работы с ним, даже если возникнет ошибка.
    with open(file_name, 'w', encoding="utf-8") as file:  # Открывает файл `file_result` в режиме записи ('w').
        # Записываем результаты в файл
        file.write(f'Сравниваемые ряды: {X_name} (х) и {Y_name} (y)\n')
        file.write(f'Корреляционное отношение {text_zn}\n')
        file.write(f'Уровень значимости: 0,05\n')
        file.write(f'Значение корреляционного отношения XY: {round(corr_ratio_XY, 3)}\n')
        file.write(f'Значение корреляционного отношения YX: {round(corr_ratio_YX, 3)}\n')
        file.write(f'95%-ный доверительный интервал для корреляционного отношения XY: '
                   f'{[round(rL, 3), round(rU, 3)]}\n')
        file.write(f'Значение η² XY: {round(corr_ratio_XY ** 2, 3)}\n')
        file.write(f'Значение η² YX: {round(corr_ratio_YX ** 2, 3)}\n')


root = tk.Tk()  # окно
root.title("Корреляционное отношение")  # заголовок окна
root.wm_minsize(400, 60)

exit_button = tk.Button(root, text="Выход", command=root.quit, font=('Arial', 14), background ='DarkSlateGray2')
exit_button.pack(side=tk.BOTTOM, pady=10)

try:
    df = pd.read_csv('../../Analiz_dannych/data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)

corr_ratio_XY = 0
corr_ratio_YX = 0
text_zn = ''
rL = 0
rU = 0
X_name = ''
Y_name = ''
X = 0
Y = 0

calculation()

root.mainloop()
