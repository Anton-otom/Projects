class D:
    __slots__ = ['a', 'b', '__dict__']
    c = 3

    def __init__(self):
        self.d = 4


X = D()
print(X.d)
