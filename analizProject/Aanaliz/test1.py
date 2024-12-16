import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_main_menu():
    clear_screen()
    os.system(r'echo Меню "Статистический анализ"')
    os.system(r'echo 1. Проверка нормальности')
    os.system(r'echo 0. Выход')


def show_normality_submenu():
    clear_screen()
    os.system(r'echo Подменю "Проверка нормальности"')
    os.system(r'echo 1. Критерий Шапиро-Уилка')
    os.system(r'echo 2. Критерий Колмогорова-Смирнова')
    os.system(r'echo 0. Назад')


def main_menu():
    while True:
        show_main_menu()
        choice = input("Введите номер пункта: ")

        if choice == '1':
            normality_check()
        elif choice == '0':
            break
        else:
            os.system(r'echo Неверный ввод. Попробуйте снова.')
            input("Нажмите Enter, чтобы продолжить...")


def normality_check():
    while True:
        show_normality_submenu()
        choice = input("Введите номер пункта: ")

        if choice == '1':
            shapiro_wilk_test()
        elif choice == '2':
            kolmogorov_smirnov_test()
        elif choice == '0':
            break
        else:
            os.system(r'echo Неверный ввод. Попробуйте снова.')
            input("Нажмите Enter, чтобы продолжить...")


def shapiro_wilk_test():
    clear_screen()
    os.system(r'echo Критерий Шапиро-Уилка')
    os.system(r'echo Выберите данные для анализа:')
    os.system(r'echo 1. Загрузить данные из файла')
    os.system(r'echo 2. Ввести данные вручную')
    os.system(r'echo 0. Назад')

    choice = input("Введите номер пункта: ")

    if choice == '1':
        load_data_from_file()
    elif choice == '2':
        enter_data_manually()
    elif choice == '0':
        return
    else:
        os.system(r'echo Неверный ввод. Попробуйте снова.')
        input("Нажмите Enter, чтобы продолжить...")


def kolmogorov_smirnov_test():
    clear_screen()
    os.system(r'echo Критерий Колмогорова-Смирнова')
    os.system(r'echo Выберите данные для анализа:')
    os.system(r'echo 1. Загрузить данные из файла')
    os.system(r'echo 2. Ввести данные вручную')
    os.system(r'echo 0. Назад')

    choice = input("Введите номер пункта: ")

    if choice == '1':
        load_data_from_file()
    elif choice == '2':
        enter_data_manually()
    elif choice == '0':
        return
    else:
        os.system(r'echo Неверный ввод. Попробуйте снова.')
        input("Нажмите Enter, чтобы продолжить...")


def load_data_from_file():
    pass  # Здесь будет реализация загрузки данных из файла


def enter_data_manually():
    pass  # Здесь будет реализация ввода данных вручную


if __name__ == "__main__":
    main_menu()