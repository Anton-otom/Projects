from class_mapattrs import mapattrs, trace


class A:
    __slots__ = ['a', 'b']; x = 1; y = 2


class B(A):
    __slots__ = ['b', 'c']


class C(A):
    x = 2


class D(B, C):
    z = 3

    def __init__(self):
        self.name = 'Bob'


I = D()
trace(mapattrs(I, bysource=True))