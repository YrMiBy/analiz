# Модуль 'select_1column'.  Выбор одного ряда из DataFrame
import tkinter as ttk
from tkinter import *
import numpy as np
import pandas as pd
from tkinter import ttk
import tkinter as tk


def center_window(window):  # Центрирование окна на экране
    window.update_idletasks()  # Обновление интерфейса
    width = 550  # Ширина окна
    height = 400
    screen_width = window.winfo_screenwidth()  # ширина экрана
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2  # координата левой верхней точки окна
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")  # Размещение окна




def column_number():  # выбор рядов с числовыми данными
    global name_column
    list_name = df.columns.tolist()  # список названий столбцов данных
    for name_column in list_name:  # перебор списка list_name для нахождения рядов с числовыми данными
        types_column = df[name_column].dtype  # определение типа данных ряда
        if types_column in [np.float64, np.int64]:  # если тип данных числовой
            # Проверка на наличие нуля и NaN
            if df[name_column].isnull().sum() > 0 or df[name_column].isna().sum() > 0:
                label = Label(root, text='В ряду {name_column} есть отсутствующие значения')
                label.pack(anchor=NW)
            else:
                list_name_number.append(name_column)  # Добавляем имя ряда в список рядов числовых данных
    #print(list_name_number)
def column_choice():  # Функция создания флажков
    global check_vars, name_column  # список состояния флажков
    try:
        col_name = len(list_name_number)  # количество названий рядов с числовыми данными
        #print(col_name)
        if col_name == 0:
            label = Label(root, text='Ряды с числовыми данными не найдены')
            label.pack()
        else:
            label = Label(root, text='Выберите ряд для анализа')
            label.pack()
            check_vars = []  # Список состояния флажков
            print(check_vars)
            for name_column in list_name_number:  # Перебор
                var = tk.BooleanVar(value=False)
                check_vars.append(var)  # Добавляем переменную в список
                # создание флажка
                enabled_checkbutton = tk.Checkbutton(root, text=name_column, variable=var, command=col_celect)
                enabled_checkbutton.pack(padx=7, pady=2, anchor=NW)
        root.bind('<Return>', on_enter_pressed)  # Привязка события нажатия Enter
    except Exception as e:
        label = Label(root, text=f'{e}')
        label.pack(anchor=NW)


def col_celect():  # Функция выбора ряда
    global name_column
    try:
        name_columns = [list_name_number[i] for i, var in enumerate(check_vars) if var.get()]
        print(name_column)
        # Удаление предыдущих сообщений.
        for widget in root.pack_slaves():
            if isinstance(widget, Label) and widget.cget("text").startswith("Выбранный ряд:"):
                widget.destroy()  # если виджет - текст начинается с "Выбранные ряды:", он удаляется

        # Проверка на количество выбранных рядов
        if len(name_columns) > 1:
            label = Label(root, text="Вы можете выбрать только один ряд.")
            label.pack(anchor=NW)
            return
        if name_columns:
            name_column = (name_columns[0])
            print(name_column)
            label = Label(root, text=f"Выбранный ряд: {name_column}")
            label.pack(anchor=NW)
            return name_column
        else:
            label = Label(root, text="Ни один ряд не выбран.")
            label.pack(anchor=NW)
    except Exception as e:
        label = Label(root, text=f'Ошибка выбора ряда: {e}')
        label.pack(anchor=NW)


def on_enter_pressed(event):  # Обработчик нажатия Enter
    end_vibor()


def end_vibor():  # функция действий после нажатия 'Enter'
    root.destroy()


def select_column(df):
    def on_select():
        nonlocal selected_column
        selected_column = combo.get()
        root.quit()
        root.destroy()

    root = tk.Tk()
    root.title("Выбор колонки")
    root.geometry("300x100")

    selected_column = None

    label = ttk.Label(root, text="Выберите колонку:")
    label.pack(pady=10)

    combo = ttk.Combobox(root, values=list(df.columns))
    combo.pack(pady=5)

    button = ttk.Button(root, text="Выбрать", command=on_select)
    button.pack(pady=10)

    root.mainloop()
    return selected_column


# Создание окна
root = Tk() # окно
root.wm_minsize(550, 300)  # минимальный размер окна
root.title("Выбор ряда")  # заголовок окна
root.iconbitmap("calculator.ico")
center_window(root)  # функция центрирования окна

# обращение к файлу data.csv, загруженному модулем loading
try:
    df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
except Exception as e:
    label = Label(root, text=f'Файл с исходными данными не найден', bg='yellow')
    label.pack(anchor=NW)

list_name_number = []  # список имен числовых рядов
check_vars = []
name_column = ''

column_number()
column_choice()
#select_column()

root.mainloop()
