"""
Для начала тестирования запустите выполнение файла в консоли.
"""
from random import shuffle
import re


# Класс цветов консоли
class Bcolors:
    # Применение форматирования {bcolors.CYAN}{....}{bcolors.END}
    END = '\033[0m'  # Обозначение места окончания применения форматирования
    BLACK = '\033[40m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    BlUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[46m'
    GRAY = '\033[47m'
    GREEN_TEXT = '\033[92m'
    CYAN_TEXT = '\033[96m'


# Функция оценки эмоционального состояния
def test_emotions(total_weight: int, user: str, colors: list):
    # Копирование списка цветов
    colors_ = colors.copy()
    # Перемешивание списка цветов
    shuffle(colors_)
    # Создание итогового списка
    results = []
    print(f'\n{"ОПРЕДЕЛЕНИЕ ЭМОЦИОНАЛЬНОГО СОСТОЯНИЯ":^{total_weight}}\n'
          f'{("Пользователь: " + user):^{total_weight}}\n\n'
          'Перед Вами 8 карточек. Пожалуйста, выберите ту карточку, которая Вам больше всего нравится.\n'
          'Вы должны выбрать цвет как таковой, не пытаясь соотнести его с любимым цветом в одежде,\n'
          'цветом глаз и т.п. После этого карточка с выбранным цветом пропадет, и Вам нужно выбрать\n'
          'уже из 7 карточек, ту которая понравится. Затем из 6-ти карточек и т.д.,\n'
          'пока все карточки не будут выбраны.')
    # Пока в списке есть цвета
    while colors_:
        print()
        # Вывод всех доступных цветов (по 4 цвета в строке)
        for id_color, color in enumerate(colors_):
            print(f'{color}{id_color + 1:^20}{Bcolors.END}', end='')
            if id_color == 3:
                print()
        # Пока в списке больше одного цвета запрашивается его номер,
        # по которому происходит удаление из списка цветов и добавление в итоговый список.
        # Если в списке 1 цвет, то удаление и добавление по индексу 0
        if len(colors_) > 1:
            # Запрос номера до тех пор, пока не будут введены правильные данные
            choice_id = input('\nВведите номер цвета: ')
            while not re.search(rf'[1-{len(colors_)}]', choice_id):
                choice_id = input('Такого номера нет, повторите ввод: ')
            results.append(colors_[int(choice_id) - 1])
            colors_.pop(int(choice_id) - 1)
        else:
            results.append(colors_[0])
            colors_.pop()
    # Возвращение результата тестирования
    return results


# Функция оценки взаимодействий в коллективе
def test_interaction(total_weight: int, user: str, colors: list, questions: list, staff: list):
    # Создание итогового словаря
    result = {}
    print(f'\n{"ВЗАИМОДЕЙСТВИЕ В КОЛЛЕКТИВЕ":^{total_weight}}\n'
          f'{("Пользователь: " + user):^{total_weight}}\n\n'
          'Перед Вами 4 вопроса. Вам нужно ответить на них. После Сделанного выбора\n'
          'необходимо поставить цвет, который Вы считаете нужным.\n'
          'Важно! Не пытайтесь угадать или найти "хороший" цвет. Его просто нет.')
    # Для каждого вопроса
    for question in questions:
        print()
        # Вывод вопроса
        print(f'{Bcolors.GREEN_TEXT}{question[1]}{Bcolors.END}')
        # Вывод списка сотрудников
        for person in staff:
            print(f'{person[0]} - {person[1]}')
        # Запрос номера до тех пор, пока не будут введены правильные данные
        choice_stuff_id = input('Введите номер сотрудника: ')
        while not re.search(r'[1-4]', choice_stuff_id):
            choice_stuff_id = input('Такого номера нет, повторите ввод: ')
        # Вывод всех доступных цветов (по 4 цвета в строке)
        for id_color, color in enumerate(colors):
            print(f'{color}{id_color + 1:^20}{Bcolors.END}', end='')
            if id_color == 3:
                print()
        # Запрос номера до тех пор, пока не будут введены правильные данные
        choice_color_id = input('\nВведите номер цвета: ')
        while not re.search(r'[1-8]', choice_color_id):
            choice_color_id = input('Такого номера нет, повторите ввод: ')
        # Заполнение итогового словаря {id вопроса: (id сотрудника, код цвета)}
        result[question[0] - 1] = (int(choice_stuff_id) - 1, colors[int(choice_color_id) - 1])
    return result


# Функция тестирования
def main():
    # Ширина вывод, для центрирования заголовков
    total_weight = 80
    # Список цветов для тестирования
    colors = [Bcolors.BLACK, Bcolors.GREEN, Bcolors.BlUE, Bcolors.YELLOW,
              Bcolors.GRAY, Bcolors.RED, Bcolors.MAGENTA, Bcolors.CYAN]
    # Список вопросов
    questions = [(1, 'Кто по вашему мнению продумывает в работе все до последней мелочи?'),
                 (2, 'Кто всегда видит детали проекта и готов копаться в мелочах?'),
                 (3, 'Кто из сотрудников доводит до конца рискованные идеи?'),
                 (4, 'С кем бы вы пошли поговорить на неформальную тему?')]
    # Список сотрудников
    staff = [(1, 'person1'), (2, 'person2'), (3, 'person3'), (4, 'person4')]
    # Запрос имени тестируемого
    user = input(f'\n{"Добрый день!":^{total_weight}}\nВведите ваши имя и фамилию: ')
    # Первое тестирование
    result_test1 = test_emotions(total_weight, user, colors)
    # Второе тестирование
    print()
    result_test2 = test_interaction(total_weight, user, colors, questions, staff)
    # Третье тестирование
    print()
    result_test3 = test_emotions(total_weight, user, colors)
    print(f'\n\n{"Спасибо за уделённое время!":^{total_weight}}\n'
          f'{"Тестирование завершено.":^{total_weight}}')

    # Вывод результатов тестирования
    print(f'\n\n{Bcolors.CYAN_TEXT}Результаты первого тестирования:{Bcolors.END}')
    for color in result_test1:
        print(f'{color}{" ":^10}{Bcolors.END}', end='')
    print(f'\n\n\n{Bcolors.CYAN_TEXT}Результаты второго тестирования:{Bcolors.END}')
    for key, value in result_test2.items():
        print(f'{questions[key][1]:<66} - {staff[value[0]][1]:<10} {value[1]}{" "* 10}{Bcolors.END}')
    print(f'\n\n{Bcolors.CYAN_TEXT}Результаты третьего тестирования:{Bcolors.END}')
    for color in result_test3:
        print(f'{color}{" ":^10}{Bcolors.END}', end='')


if __name__ == '__main__':
    main()
