# Модуль 'anova'. Однофакторный дисперсионный анализ
from scipy.stats import f_oneway
import pandas as pd
from tkinter import *


def open_file(statistics, p_value, text_rez):  # Файл вывода результатов
    file_name = "file_result.txt"
    with open(file_name, 'w', encoding="utf-8") as file:
        # Записываем результаты в файл
        file.write(f'Уровень значимости: 0,05\n')
        file.write(f'Статистика: {round(statistics, 5)}\n')
        file.write(f'P-значение: {round(p_value, 5)}\n')
        file.write(text_rez)


def create_label(text, color='DarkSlateGray2'):  # параметры виджетов
    return Label(root_anova, text=text, bg=color, font=('Calibri', 12))


# Создание окна
root_anova = Tk()
root_anova.geometry(f'500x130')
root_anova.title("Дисперсионный анализ")
root_anova.iconbitmap("calculator.ico")
root_anova.eval('tk::PlaceWindow . center')  # центрирование окна
root_anova.config(bg='DarkSlateGray2')  # Цвет фона

try:
    df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)

try:
    num_columns = df.shape[1]  # Количество столбцов в файле (групп)
    groups = []  # Список для хранения групп

    # Формируем список групп
    for index in range(num_columns):
        groups.append(df.iloc[:, index].tolist())  # Используем iloc для доступа по индексу
    statistics, p_value = f_oneway(*groups)
    if df.isnull().values.any():
        label = create_label('Ошибка в исходном файле', 'yellow')
        label.pack(anchor=NW)
    else:
        label = Label(root_anova, text='Результаты дисперсионного анализа:' , font=('Calibri', 14), bg='DarkSlateGray2')
        label.pack(anchor=NW)

        text_st = f'Значение критерия Фишера: {round(statistics, 5)}'
        label = create_label(text_st)
        label.pack(anchor=NW)

        text_p = f'P-значение: {round(p_value, 5)}'
        label = create_label(text_p)
        label.pack(anchor=NW)

        if p_value > 0.05:
            text_rez = 'Различия между группами не значимы на уровне 95%'
        else:
            text_rez = 'Различия между группами значимы на уровне 95%'

        label = create_label(text_rez)
        label.pack(anchor=NW)

        open_file(statistics, p_value, text_rez)
except:
    text_err = 'Ошибка в исходном файле'
    label = create_label(text_err)
    label.pack(anchor=NW)

root_anova.mainloop()
