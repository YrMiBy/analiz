# Модуль 'select_2column'
# Выбор 2 рядов для их анализа
import tkinter as ttk
from tkinter import *
import numpy as np
import pandas as pd


def center_window(window):  # Центрирование окна на экране
    try:
        window.update_idletasks()  # Обновление интерфейса
        width = window.winfo_width()  # Ширина окна
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()  # ширина экрана
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2  # координата левой верхней точки окна
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")  # Размещение окна
    except Exception as e:
        label = Label(root, text=f'Ошибка центрирования фрейма: {e}', anchor=NW, bg='yellow')
        label.pack(anchor=NW)  # Показываем ошибку пользователю


root = ttk.Tk()  # окно
root.wm_minsize(550, 300)  # минимальный размер окна
root.title("Выбор рядов")  # заголовок окна
center_window(root)


def column_number():  # выбор рядов с числовыми данными
    list_name = df.columns.tolist()  # список названий столбцов данных
    for name_column in list_name:  # перебор списка list_name для нахождения рядов с числовыми данными
        types_column = df[name_column].dtype  # определение типа данных ряда
        if types_column in [np.float64, np.int64]:  # если тип данных числовой (с плавающей точкой или целые)
            # Проверка на наличие значений, отличных от нуля и Nan
            # Проверка на наличие нуля и NaN
            if df[name_column].isnull().sum() > 0 or df[name_column].isna().sum() > 0:
                label = Label(root, text=f'В ряду {name_column} есть отсутствующие значения')
                label.pack(anchor=NW)
            else:
                list_name_number.append(name_column)  # Добавляем имя ряда в список рядов числовых данных


def column_choice():  # Выбор рядов для анализа
    global check_vars
    try:
        col_name = len(list_name_number)  # количество названий рядов с числовыми данными
        if col_name == 0:
            label = Label(root, text='Ряды с числовыми данными не найдены', bg='yellow')
            label.pack()
        elif col_name == 1:
            label = Label(root, text='Найден только 1 ряд с числовыми данными', bg='yellow', )
            label.pack()
        else:
            label = Label(root, text='Выберите 2 ряда для анализа', bg='light blue')
            label.pack()
            check_vars = []   # Список состояния флажков
            for name_column in list_name_number:  # Перебор
                var = ttk.BooleanVar(value=False)  # Переменная состояния флажка. Изначально выключен (False)
                check_vars.append(var)  # Добавляем переменную в список
                enabled_checkbutton = ttk.Checkbutton(text=name_column, variable=var,
                                                      command=col_celect)  # создание флажка
                enabled_checkbutton.pack(padx=10, pady=3, anchor=NW)  # Прорисовка флажка
        root.bind('<Return>', on_enter_pressed)  # Привязка события нажатия Enter
    except Exception as e:
        label = Label(root, text=f'Ошибка выбора рядов: {e}', anchor=NW, bg='yellow')
        label.pack(anchor=NW)  # Показываем ошибку пользователю


def col_celect():
    global name_columns
    try:
        # Создание списка выбранных рядов (описание в модуле selecting_column)
        name_columns = [list_name_number[i] for i, var in enumerate(check_vars) if var.get()]
        # Удаление предыдущих сообщений (описание фв модуле selecting_column)
        for widget in root.pack_slaves():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбранные ряды:"):
                widget.destroy()  # если виджет - метка и текст начинается с "Выбранные ряды:", он удаляется (destroy)
        if len(name_columns) > 2:  # Проверка на количество выбранных рядов
            label = Label(root, text="Вы можете выбрать только два ряда.")
            label.pack(anchor=NW)
            return
        elif len(name_columns) == 1:
            label = Label(root, text="Выбран только 1 ряд")
            label.pack(anchor=NW)
        elif name_columns:
            selected_text = ', '.join(name_columns)  # объединение элементов списка selected_columns в строку
            label = Label(root, text=f"Выбранные ряды: {selected_text}")
            label.pack(anchor=NW)
            return name_columns
        else:
            label = Label(root, text="Ни один ряд не выбран.")
            label.pack(anchor=NW)
    except Exception as e:
        label = Label(root, text=f'Ошибка выбора рядов: {e}')
        label.pack(anchor=NW)  # Показываем ошибку пользователю


def on_enter_pressed(event):  # Обработчик нажатия Enter
    end_choice()


def end_choice():  # функция действий после нажатия 'Enter'
    global name_columns
    name_columns = get_name_columns()
    root.destroy()


def get_name_columns():  # Возвращает список выбранных рядов
    return name_columns


# Глобальная переменная для хранения выбранных рядов
name_columns = ''
check_vars = []
list_name_number = []  # список имен числовых рядов
# обращение к файлу data.csv, загруженному модулем loading
df = pd.read_csv('data.csv')

column_number()
column_choice()

root.mainloop()
