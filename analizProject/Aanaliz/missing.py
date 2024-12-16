# Модуль missing
# Определение рядов с пропущенными данными и действия с ними (удаление, замена средним или медианой)
import pandas as pd
import tkinter as ttk
from tkinter import scrolledtext
from tkinter import *
import numpy as np


def center_window(window):  # Центрирование окна на экране
    window.update_idletasks()  # Обновление интерфейса
    width = window.winfo_width()  # Ширина окна
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()  # ширина экрана
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2  # координата левой верхней точки окна
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")  # Размещение окна


def missings_data():
    # Определение отсутствующих данных
    missing_data = df.isnull().sum()

    # Создание текстового поля с прокруткой
    text_area = scrolledtext.ScrolledText(root)
    text_area.pack(padx=10, pady=10)

    # Заполнение текстового поля результатами
    text_area.insert(ttk.END, "Количество отсутствующих данных в каждом столбце:\n")
    text_area.insert(ttk.END, str(missing_data))

    # Запрет редактирования текста
    text_area.config(state=ttk.DISABLED)


def delit_string():
    # Удаление записей с отсутствующими данными
    df_cleaned = df.dropna()
    # Сохранение очищенного DataFrame в новый CSV файл
    df_cleaned.to_csv('data_cleaned.csv', index=False)


def average_string():
    # Определение пропущенных значений и создание переменной индикатора пропущенных значений.
    df_numeric = df.select_dtypes(include=[np.number])  # Отбор числовых столбцов
    numeric_cols = df_numeric.columns.values  # список наименований числовых столбцов

    for col in numeric_cols:
        missing = df[col].isnull()  # проверка пропущенных значений в столбце
        num_missing = np.sum(missing)  # сумма пропущенных значений

    # Вычисление среднего только для тех столбцов, в которых отсутствуют значения.
        if num_missing > 0:
            df['{}_ismissing'.format(col)] = missing
            mean_column = df[col].mean()
            df[col] = df[col].fillna(round(mean_column, 4))
        # Сохранение очищенного DataFrame в новый CSV файл
    df.to_csv('data_cleaned.csv', index=False)


def median_string():
    # Определение пропущенных значений и создание переменной индикатора пропущенных значений.
    df_numeric = df.select_dtypes(include=[np.number])  # Отбор числовых столбцов
    numeric_cols = df_numeric.columns.values  # список наименований числовых столбцов

    for col in numeric_cols:
        missing = df[col].isnull()  # проверка пропущенных значений в столбце
        num_missing = np.sum(missing)  # сумма пропущенных значений

        # Вычисление медианы только для тех столбцов, в которых отсутствуют значения.
        if num_missing > 0:
            df['{}_ismissing'.format(col)] = missing
            mean_column = df[col].median()
            df[col] = df[col].fillna(round(mean_column, 4))
    # Сохранение очищенного DataFrame в новый CSV файл
    #df_new.to_csv('data_new.csv', index=False)


def button_missing():  # Выбор вариантов редактирования
    label = Label(root, text=f'Варианты редактирования:')
    label.pack(anchor=NW)
    Button(root, text="Удаление записей", command=delit_string).place(x=160, y=0)
    Button(root, text="Замена средним", command=average_string).place(x=270, y=0)
    Button(root, text="Замена медианой", command=median_string).place(x=374, y=0)

# Создание окна
root = ttk.Tk()  # Главное окно
root.title("Отсутствующие данные")  # заголовок окна
root.wm_minsize(600, 200)  # min размер окна
center_window(root)  # функция центрирования окна

try:
    df = pd.read_csv('../../Analiz_dannych/data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)

button_missing()
missings_data()


root.mainloop()
