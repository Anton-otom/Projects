# a_b = input().split()
# print(int(a_b[0]) + int(a_b[1]))
# ______________________________________________________________________________________________________________________

# with open("input.txt", "r") as input_file, open("output.txt", "w") as output_file:
#     a_b = input_file.readline().split()
#     sum_a_b = int(a_b[0]) + int(a_b[1])
#     output_file.write(str(sum_a_b))
# ______________________________________________________________________________________________________________________

# a_b = input().split()
# print(int(a_b[0]) + int(a_b[1]))
# ______________________________________________________________________________________________________________________

# J = list(input())
# S = list(input())
# result = 0
# for symbol in S:
#     if symbol in J:
#         result += 1
# print(result)
# ______________________________________________________________________________________________________________________
# t_room, t_cond = map(int, input().split())
# mod_k = input()
# if mod_k == "freeze":
#     if t_room > t_cond:
#         t_room = t_cond
# elif mod_k == "heat":
#     if t_room < t_cond:
#         t_room = t_cond
# elif mod_k == "auto":
#     t_room = t_cond
# elif mod_k == "fan":
#     pass
#
# print(t_room)
# ______________________________________________________________________________________________________________________
# a = int(input())
# b = int(input())
# c = int(input())
#
# if (a + b > c) and (a + c > b) and (b + c > a):
#     print('YES')
# else:
#     print('NO')
# ______________________________________________________________________________________________________________________
# new_number = ''.join(input().split("-"))
# old_number1 = ''.join(input().split("-"))
# old_number2 = ''.join(input().split("-"))
# old_number3 = ''.join(input().split("-"))
#
#
# def standart(number: str):
#     if len(number) == 7:
#         number = '495' + number
#     else:
#         if number[0] == '+':
#             number = number[2:]
#         else:
#             number = number[1:]
#         if number[0] == '(':
#             number = number[1:4] + number[5:]
#     return number
#
#
# new_number = standart(new_number)
# book_number = [old_number1, old_number2, old_number3]
# for num in book_number:
#     num = standart(num)
#     if num == new_number:
#         print('YES')
#     else:
#         print('NO')
# ______________________________________________________________________________________________________________________
# def buielder(name: str, size: int):
#     for i in range(size):
#         name += input() + '|'
#     return name
#
#
# def comparison(data: str, requests: str):
#     counter_actions = [0]
#     for token_req in requests:
#         if token_req == '|':
#             counter_actions.append(0)
#             continue
#         for token_base in data:
#             counter_actions[-1] += 1
#             if token_req != token_base:
#                 return counter_actions
#
#
# size_base, data_base = int(input()), ''
# data_base = buielder(data_base, size_base)
# number_requests, text_requests = int(input()), ''
# text_requests = buielder(text_requests, number_requests)
# print(data_base)
# print(text_requests)
# print(comparison(data_base, text_requests))
# # counter_actions = [0]
# ______________________________________________________________________________________________________________________

# # Функция заполнения базы данных size раз. Возвращает заполненную базу данных
# def buielder(name: list, size: int):
#     for i in range(size):
#         name.append(input())
#     return name
#
#
# # Функция запуска цикла сравнения слова из запроса и каждого слова из базы данных.
# # (база данных, база запросов)
# def comparison_data(data: list, requests: list):
#     # Инициализация переменной-счетчика действий
#     counter_actions = []
#     for word_req in requests:
#         # Создание счётчика действий для конкретного слова из запроса
#         counter_actions.append(0)
#         # Вызов функции сравнения слова запроса и слов базы данных.
#         # (база данных, слово из запроса, счётчик действий)
#         comparison_word(data, word_req, counter_actions)
#     return counter_actions
#
#
# # Функция сравнения слова запроса и слов базы данных.
# # (база данных, слово из запроса, счётчик действий)
# def comparison_word(data: list, word_req: list, counter_actions: list):
#     for word_data in data:
#         # Если слово запроса равно по длине слову из базы данных
#         if len(word_req) == len(word_data):
#             # Поиндексно сравниваем буквы двух слов
#             for i in range(len(word_req)):
#                 counter_actions[-1] += 1
#                 # Если не совпадение, переход к следующему слову из базы данных
#                 if word_req[i] != word_data[i]:
#                     break
#                 # Если совпадение и это НЕ последняя буква запроса, то продолжаем сравнение элементов
#                 else:
#                     # Если совпадение и это последняя буква запроса,
#                     # увеличиваем счетчик и переходим к следующему слову запроса
#                     if i == len(word_req) - 1:
#                         counter_actions[-1] += 1
#                         #
#                         return
#         # Если слово запроса НЕ равно по длине слову из базы данных,
#         # то увеличиваем счётчик действий и переходим к следующему слову запроса
#         else:
#             counter_actions[-1] += 1
#             return
#     return
#
#
# # Запрос размера и создание пустой базы данных
# size_base, data_base = int(input()), []
# # Заполнение базы данных
# data_base = buielder(data_base, size_base)
# # Запрос размера и создание пустой базы данных
# number_requests, text_requests = int(input()), []
# # Заполнение базы данных
# text_requests = buielder(text_requests, number_requests)
# # Получение списка с количеством сравнений по каждому слову и его поэлементный вывод
# for j in comparison_data(data_base, text_requests):
#     print(j)
# ______________________________________________________________________________________________________________________
row, col = list(map(int, input().split()))
words_list = []
for i in range(row):
    words_list.append(list(input()))
for j in range(col):
    words_list.append([])
    for i in range(row):
        words_list[row + j].append(words_list[i][j])
for id_word, word in enumerate(words_list):
    words_list[id_word] = ''.join(word)
for id_word, word in enumerate(words_list):
    bag_id_list = []
    for id_char, char in enumerate(words_list[id_word]):
        if char == '#':
            bag_id_list.append(id_char)
    for id_bag in bag_id_list:
        if (id_bag - 2 < 2) or (id_bag + 2 > col - 1):
            words_list.pop(id_word)
            continue
    words_list[id_word].replace('#', '')
    if len(words_list[id_word]) < 2:
        words_list.pop(id_word)
words_list = sorted(words_list)
print(words_list[0])