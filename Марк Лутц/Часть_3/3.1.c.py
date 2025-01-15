S = input('Введите строку: ')
dict_ = {}

for s in S:
    dict_[s] = ord(s)
else:
    print('ASCII коды символов в строке: ', dict_)

print()
print(list(map(ord, S)))

print()
print([ord(c) for c in S])


