# Модуль main. Меню для выбора вариантов анализа
from tkinter import *
from tkinter import Tk
import importlib

def normaltest_menu():  # Модуль "Проверка нормальности"
    import select_1column
    #select_1column.start_select_1column()
    # import normaltest
    # normaltest.start_normaltest()

# Создание главного окна
root = Tk()
# Центрирование окна на экране
root.eval('tk::PlaceWindow . center')
root.geometry('315x100')
#root.iconbitmap("calculator.ico")
root.title("Анализ данных")
root.option_add("*tearOff", FALSE)

# Устанавливаем шрифт по умолчанию для всех виджетов
font = ("Areal", 12)
root.option_add("*Font", font)

# Создание главного меню
main_menu = Menu(root)
root.config(menu=main_menu)

# Меню "Статистический анализ"
statanaliz = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Статистический анализ", menu=statanaliz)
statanaliz.add_command(label="Проверка номальности", command=normaltest_menu)

root.config(menu=main_menu)
root.mainloop()

