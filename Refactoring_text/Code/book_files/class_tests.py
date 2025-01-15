class propeties(object):
    def getage(self):
        return 40

    def setage(self, value):
        print(f'Set age: {value}')
        self._age = value

    age = property(getage, setage, None, 'Hello')


x = propeties()
print(x.age)
x.age = 42
