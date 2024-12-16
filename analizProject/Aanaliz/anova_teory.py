# Модуль anova_teory.py. Пояснения к дисперсионному анализу
import tkinter as ttk
from tkinter import *


def center_window(root):  # Центрирование окна на экране
    root.update_idletasks()  # Обновление интерфейса
    screen_width = root.winfo_screenwidth()  # ширина экрана
    screen_height = root.winfo_screenheight()
    # Устанавливаем ширину и высоту окна
    window_width = screen_width-100
    window_height = screen_height-300
    # Вычисляем координаты для центрирования окна
    x_cord = int((screen_width / 2) - (window_width / 2))
    y_cord = int((screen_height / 2) - (window_height / 2))
    # Устанавливаем геометрию окна
    root.geometry(f"{window_width}x{window_height}+{x_cord}+{y_cord}")


root = Tk()
center_window(root)
root.title("Дисперсионный анализ")
root.iconbitmap("calculator.ico")

text = ttk.Text(root, wrap='word', bg='DarkSlateGray2', font=('Calibri', 12))  # перенос по словам, цвет фона, шрифт
text.pack(expand=True, fill='both', padx=20, pady=20)

description = """   
    ### Дисперсионный анализ (ANOVA) ###

    Дисперсионный анализ (ANOVA) позволяет определить, существует ли значимое различие между группами данных (выборками), 
    характеризующимися качественными признаками переменной.

    Для проведения дисперсионного анализа необходимо загрузить файл 'excel' следующего вида:
    
        group1                 group2	                  ...
        значение 1_1    значение2_1         ...
        значение 1_2    значение2_2         ...
        значение 1_3    значение2_3         ...
        значение 1_4    значение2_4         ...
        ...                              ...
        где:
        - "group1", "group2", и так далее - имена групп данных (выборок);
        - "значение" - полученные значения результативного признака (y).
        
    Размеры групп данных должны быть одинаковыми.

    В программе:
     1. Проверяется однородность дисперсий групп данных
     2. Результаты анализа выводятся на экран и в текстовый файл "file_rezuln.txt"      
   """
text.insert('1.0', description)
text.config(state='disabled')

root.mainloop()
