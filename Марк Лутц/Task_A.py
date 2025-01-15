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