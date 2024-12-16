# Модуль emission
# Определение выбросов с использованием межквартильного размаха
import tkinter as ttk
from tkinter import *
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import select_1column
import seaborn as sbn

# Загрузка файла data.csv, загруженного модулем loading
try:
    df = pd.read_csv('../../Analiz_dannych/data.csv')
except FileNotFoundError:
    exit(1)

name_column = select_1column.name_column  # Выбор ряда в модуле select_1column


# Расчет выбросов
def calculasion():
    global ucl, lcl, col_ucl, col_lcl
    try:
        q1 = df[name_column].quantile(q=.25)  # Квртиль 0,25
        q3 = df[name_column].quantile(q=.75)
        IQR = q3 - q1   # Межквартильный размах
        ucl = q3+1.5*IQR   # Верхняя допустимая граница значений
        lcl = q1-1.5*IQR  # Нижняя допустимая граница значений
        col_ucl = (df[name_column] > ucl).sum()  # Количество значений выше верхней границы
        col_lcl = (df[name_column] < lcl).sum()  # Количество значений ниже нижней границы

        if col_ucl > 0 or col_lcl > 0:
            frame_root()
            button_emis()
        else:
            label = Label(root, text='Выбросов нет', bg='DarkSlateGray2', font=('Arial', 12))
            label.pack()
    except Exception as e:
        label = Label(root, text=f'Ошибка в вычислении: {e}')
        label.pack(anchor=NW)


def frame_root():  # Размещение графика и окна на экране
    global frame_controls
    # Создание фрейма для графика
    frame_graph = ttk.Frame(root)  # фрейм для графика
    frame_graph.pack(side=ttk.LEFT, fill=ttk.BOTH, expand=True)
    # Создание нового виджета для размещения окна с результатами
    frame_controls = ttk.Frame(root)
    frame_controls.pack(side=ttk.RIGHT, fill=ttk.X)
    # Создание графика
    fig, ax = plt.subplots()
    sbn.boxplot(df[name_column])
    # Встраивание графика в tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame_graph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=ttk.BOTH, expand=True)
    # Размещение окна с данными
    result_text = f"""
        Ряд : {name_column} 
        Верхняя предельная граница: {ucl}
        Нижняя предельная граница: {lcl}
        Количество значений выше верхней границы: {col_ucl}
        Количество значений ниже нижней границы: {col_lcl}
        """
    label = Label(frame_controls, text=result_text, justify=LEFT, font=('Arial', 14))
    label.pack(anchor=NW)


def button_emis():  # Запрос на удаление выбросов
    label = Label(frame_controls, text='Удалить выбросы?', bg='DarkSlateGray2', font=('Arial', 14))
    label.pack(side=LEFT, pady=10)
    button_yes = Button(frame_controls, text='да', font=('Arial', 14), command=yes_string)
    button_yes.pack(side=LEFT, padx=5)
    button_no = Button(frame_controls, text='нет', font=('Arial', 14), command=no_string)
    button_no.pack(side=LEFT, padx=5)


def yes_string():  # Удаление выбросов (кнопка 'да')
    df_new = df[(df[name_column] >= lcl) & (df[name_column] <= ucl)]  # Новый фрейм с удаленными строками
    #df_new.to_csv('data_new.csv', index=False)  # Сохраняем файл в файл data.csv


def no_string():  # кнопка 'нет'
    pass


# Создание окна
root = ttk.Tk()  # окно
root.wm_minsize(550, 150)  # минимальный размер окна
root.title("Выбросы")  # заголовок окна

exit_button = ttk.Button(root, text="Выход", command=root.quit, font=('Arial', 14), bg='DarkSlateGray2')
exit_button.pack(side=ttk.BOTTOM, pady=10)

ucl = 0
lcl = 0
col_ucl = 0
col_lcl = 0

calculasion()

root.mainloop()
