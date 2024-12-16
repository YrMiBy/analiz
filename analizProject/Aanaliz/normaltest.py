# Модуль 'normaltest'. Проверка ряда на нормальность
import tkinter as ttk
from tkinter import *
import pandas as pd
import scipy.stats as stats
import seaborn as sbn
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import select_1column


def start_normaltest():
    def calculation():  # Расчет
        global chap, p, text_result
        try:
            n = df[name_column].count()  # определение объема выборки
            if n > 3:
                chap, p = stats.shapiro(df[name_column])  # тест Шапиро-Уилка
                if p < 0.05:
                    text_result = 'не соответствует'
                else:
                    text_result = 'соответствует'
            else:
                label = ttk.Label(root_norm, text=f'Данных должно быть больше 3', bg='yellow')
                label.pack()
        except Exception as e:
            text = f'{e}'

    root_norm = ttk.Tk()  # окно
    root_norm.wm_minsize(1600, 200)
    root_norm.title("Проверка нормальности ряда")
    #root_norm.iconbitmap("calculator.ico")

    try:
        df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
    except FileNotFoundError as e:
        exit(1)

    # Сначала выбираем колонку
    name_column = select_1column.name_column(df) # Выбор ряда в модуле 'select_1column'
    if name_column:
        print(name_column)


        exit_button = ttk.Button(root_norm, text="Выход", command=root_norm.quit,
                                 font=('Calibri', 12), bg='DarkSlateGray2')
        exit_button.pack(side=ttk.BOTTOM, pady=10)

        chap = 0
        p = 0
        text_result = ''
        frame_controls = 0
        result_text = ''

        calculation()
        root_norm.mainloop()
    else:
        root_norm.destroy()