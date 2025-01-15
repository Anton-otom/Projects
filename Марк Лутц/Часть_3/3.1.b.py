S = input('Введите строку: ')
sum_ = 0

for s in S:
    print(ord(s), end=' ')
    sum_ += ord(s)
else:
    print()
    print(sum_)

