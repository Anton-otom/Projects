# Функция заполнения базы данных size раз. Возвращает заполненную базу данных
def buielder(name: list, size: int):
    for i in range(size):
        name.append(input())
    return name


# Функция запуска цикла сравнения слова из запроса и каждого слова из базы данных.
# (база данных, база запросов)
def comparison_data(data: list, requests: list):
    # Инициализация переменной-счетчика действий
    counter_actions = []
    for word_req in requests:
        # Создание счётчика действий для конкретного слова из запроса
        counter_actions.append(0)
        # Вызов функции сравнения слова запроса и слов базы данных.
        # (база данных, слово из запроса, счётчик действий)
        comparison_word(data, word_req, counter_actions)
    return counter_actions


# Функция сравнения слова запроса и слов базы данных.
# (база данных, слово из запроса, счётчик действий)
def comparison_word(data: list, word_req: list, counter_actions: list):
    for word_data in data:
        # Если слово запроса равно по длине слову из базы данных
        if len(word_req) == len(word_data):
            # Поиндексно сравниваем буквы двух слов
            for i in range(len(word_req)):
                counter_actions[-1] += 1
                # Если не совпадение, переход к следующему слову из базы данных
                if word_req[i] != word_data[i]:
                    break
                # Если совпадение и это НЕ последняя буква запроса, то продолжаем сравнение элементов
                else:
                    # Если совпадение и это последняя буква запроса,
                    # увеличиваем счетчик и переходим к следующему слову запроса
                    if i == len(word_req) - 1:
                        counter_actions[-1] += 1
                        #
                        return
        # Если слово запроса НЕ равно по длине слову из базы данных,
        # то увеличиваем счётчик действий и переходим к следующему слову запроса
        else:
            counter_actions[-1] += 1
            return
    return


# Запрос размера и создание пустой базы данных
size_base, data_base = int(input()), []
# Заполнение базы данных
data_base = buielder(data_base, size_base)
# Запрос размера и создание пустой базы данных
number_requests, text_requests = int(input()), []
# Заполнение базы данных
text_requests = buielder(text_requests, number_requests)
# Получение списка с количеством сравнений по каждому слову и его поэлементный вывод
for j in comparison_data(data_base, text_requests):
    print(j)