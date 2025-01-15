def mysum(L):
    print(L)
    if not L:
        return 0
    else:
        return L[0] + mysum(L[1:])


def mysum(L):
    return 0 if not L else L[0] + mysum(L[1:])


def mysum(L):
    return L[0] if len(L) == 1 else L[0] + mysum(L[1:])


def mysum(L):
    first, *rest = L
    return first if not rest else first + mysum(rest)


def mysum(L):
    if not L:
        return 0
    return nonempty(L)


def nonempty(L):
    return L[0] + mysum(L[1:])


def sumtree(L):
    tot = 0
    for x in L:
        if not isinstance(x, list):
            tot += x
        else:
            tot += sumtree(x)
    return tot


L = [1, [2, [3, 4], 5], 6, [7, 8]]
print(sumtree(L))
print(sumtree([1, [2, [3, [4, [5]]]]]))
print(sumtree([[[[[1], 2], 3], 4], 5]))


def sumtree(L):
    tot = 0
    items = list(L)
    while items:
        front = items.pop(0)
        if not isinstance(front, list):
            tot += front
        else:
            items.extend(front)
    return tot


def sumtree(L):
    tot = 0
    items = list(L)
    while items:
        front = items.pop(0)
        if not isinstance(front, list):
            tot += front
        else:
            items[:0] = front
    return tot

L = [[1, 2, 3], [4, 5, 6]]
M = [[1, 2, 3],
     [4, 5, 6],
     [7, 8, 9]]
N = [[2, 2, 2],
     [3, 3, 3],
     [4, 4, 4]]

a = [col + 10 for row in M for col in row]
print(a)
b = [[col + 10 for col in row] for row in M]
print(b)


def gensquares(N):
    for i in range(N):
        yield i ** 2


def scramble(seq):
    res = []
    for i in range(len(seq)):
        res.append(seq[1:] + seq[:1])
    return res


scramble('spam')


def scramble(seq):
    return [seq[i:] + seq[:i] for i in range(len(seq))]


scramble('spam')

for x in scramble((1, 2, 3)):
    print(x, end=' ')


def scramble(seq):
    for i in range(len(seq)):
        seq = seq[1:] + seq[:1]
        yield seq


def scramble(seq):
    for i in range(len(seq)):
        yield seq[i:] + seq[:i]


list(scramble('spam'))
list(scramble((1, 2, 3)))

for x in scramble((1, 2, 3)):
    print(x, end=' ')


def scramble(seq):
    for i in range(len(seq)):
        yield seq[i:] + seq[:i]


scramble2 = lambda seq: (seq[i:] + seq[:i] for i in range(len(seq)))
