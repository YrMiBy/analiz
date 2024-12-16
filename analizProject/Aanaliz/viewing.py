import tkinter as ttk
import csv
import pandas as pd


try:
    df = pd.read_csv('data.csv')  # Файл data.csv, загруженный модулем loading
except FileNotFoundError:
    exit(1)


def create_frame():
    # Создаем главное окно
    root = ttk.Tk()
    root.title("Просмотр DataFrame")

    # Создаем фрейм
    frame = ttk.Frame(root, padx=10, pady=10)
    frame.grid(padx=20, pady=20)  # Используем grid

    # Читаем данные из файла data.csv
    with open('data.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        # Читаем заголовки
        headers = next(reader)

        # Создаем рамку для заголовков и значений
        header_frame = ttk.Frame(frame)
        header_frame.grid(row=5, column=0, pady=10)  # Размещаем рамку заголовков с помощью grid

        # Создаем метки заголовков
        for j, header in enumerate(headers):
            label_header = ttk.Label(header_frame, text=header)  # Заголовок
            label_header.grid(row=0, column=j, padx=5, pady=5, sticky='n')

        # Читаем и выводим данные с заголовками
        for i, row in enumerate(reader):
            if i < 5:  # Выводим только первые 5 строк
                row_frame = ttk.Frame(frame)  # Создаем новый фрейм для строки
                row_frame.grid(row=6 + i, column=0)  # Размещаем фрейм строки с помощью grid
                for j, value in enumerate(row):  # Переменная value - это строка
                    # Создаем метку для значения
                    label_value = ttk.Label(row_frame, text=value)  # Значение
                    label_value.grid(row=0, column=j, padx=5, pady=5, sticky='n')
            else:
                break  # Прерываем цикл после 5 строк

    # Запускаем главный цикл приложения
    root.mainloop()

#display(df.head())  #проверить вывод фрейма на дисплей

# Вызов функции для создания фрейма
create_frame()
