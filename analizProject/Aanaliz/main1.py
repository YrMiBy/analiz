# Модуль main. Меню для выбора вариантов анализа
from tkinter import *
from tkinter import Tk
import importlib


def reload_module(module_name):
    module = importlib.import_module(module_name)
    importlib.reload(module)


def loadings():  # Модуль "Загрузка файла"
    reload_module('loading')


def eda_menu():  # Модуль "Разведывательный анализ"
    import eda   # noqa


def missing_menu():  # Модуль "Анализ пропущенных данных"
    import missing


def emissions_menu():  # Модуль "Анализ выбросов"
    import emissions


def normaltest_menu():  # Модуль "Проверка нормальности"
    import normaltest
    #reload_module('normaltest')


def podgonka_menu():  # Модуль "Подгонка распределения"
    import podgonka_ks  # noqa


def regrssion_teoriy_menu():  # Модуль "Описание линейных регрессии и корреляции"
    import regression_teoriy


def regrssion_menu():  # Модуль "Расчет линейных регрессии и корреляции"
    import regression


def relation_teoriy_menu():  # Модуль "Описание корреляционного отношения"
    import correl_teory


def relation_menu():  # Модуль "Расчет корреляционного отношения"
    import correl_relation


def anova_teoriy_menu():  # Модуль "Описание дисперсионного анализа"
    import anova_teory


def anova_menu():  # Модуль "Расчет дисперсионного анализа"
    import anova


def doe_teoriy_menu():  # Модуль "Описание планирования эксперимента"
    import doe_teory


def doe_menu():  # Модуль "Расчет планирования эксперимента"
    import doe


# Создание главного окна
root = Tk()
# Центрирование окна на экране
root.eval('tk::PlaceWindow . center')
# Размеры окна, иконка, титул
root.geometry(f'315x100')
root.iconbitmap("calculator.ico")
root.title("Анализ данных")
root.option_add("*tearOff", FALSE)

# Устанавливаем шрифт по умолчанию для всех виджетов
font = ("Calibri", 12)
root.option_add("*Font", font)

# Создание главного меню
main_menu = Menu(root)
root.config(menu=main_menu)

# Меню "Файл"
loading_menu = Menu(main_menu, tearoff=0)  # tearoff=0 отключает возможность открепления подменю от меню
main_menu.add_cascade(label="Файл", menu=loading_menu)
loading_menu.add_command(label='Загрузка DataFrame', command=loadings)
loading_menu.add_separator()
loading_menu.add_command(label="Выход", command=root.destroy)

# Меню "Проверка нормальности"
loading_menu = Menu(main_menu, tearoff=0)  # tearoff=0 отключает возможность открепления подменю от меню
main_menu.add_command(label="Проверка нормальности", command=normaltest_menu)


# Меню "Обработка данных"
obrabotka_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Обработка данных", menu=obrabotka_menu)
obrabotka_menu.add_command(label='Разведывательный анализ', command=eda_menu)
obrabotka_menu.add_command(label='Анализ пропущенных данных', command=missing_menu)
obrabotka_menu.add_command(label='Анализ выбросов', command=emissions_menu)

# Меню "Статистический анализ"
statanaliz = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label="Статистический анализ", menu=statanaliz)
statanaliz.add_command(label="Проверка номальности", command=normaltest_menu)
statanaliz.add_command(label="Подгонка распределения", command=podgonka_menu)

# Подменю "Линейные корреляция и регрессия" меню "Статистический анализ"
correl = Menu(statanaliz, tearoff=0)
statanaliz.add_cascade(label="Линейные корреляция и регрессия", menu=correl)
correl.add_command(label="Описание", command=regrssion_teoriy_menu)
correl.add_command(label="Расчет", command=regrssion_menu)

# Подменю "Корреляционное отношение" меню "Статистический анализ"
relation_correl = Menu(statanaliz, tearoff=0)
statanaliz.add_cascade(label="Корреляционное отношение", menu=relation_correl)
relation_correl.add_command(label="Описание", command=relation_teoriy_menu)
relation_correl.add_command(label="Расчет", command=relation_menu)

# Подменю "Дисперсионный анализ" меню "Статистический анализ"
menu_anova = Menu(statanaliz, tearoff=0)
statanaliz.add_cascade(label="Дисперсионный анализ", menu=menu_anova)
menu_anova.add_command(label="Описание", command=anova_teoriy_menu)
menu_anova.add_command(label="Расчет", command=anova_menu)

# Подменю "Планирование эксперимента" меню "Статистический анализ"
menu_doe = Menu(statanaliz, tearoff=0)
statanaliz.add_cascade(label="Планирование эксперимента", menu=menu_doe)
menu_doe.add_command(label="Описание", command=doe_teoriy_menu)
menu_doe.add_command(label="Расчет", command=doe_menu)

root.config(menu=main_menu)  # Установка меню для текущего окна
root.mainloop()

if __name__ == "__main__":
    main()
