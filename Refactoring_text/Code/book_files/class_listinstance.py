if __name__ != '__main__':
    print('-' * 60)
    print(f'Вы импортировали модуль: "{__name__}"')
    print('-' * 60)


class ListInstance:
    """
    Подмешиваемый класс, который предоставляет форматированную функцию
    print() или str() для экземпляров через наследование реализованного
    в нём метода __str__; отображает только атрибуты экземпляа; self
    является экземпляром самого нижнего класса;
    имена __X предоставляют конфликты с атрибутами клиента
    """
    def __attrnames(self):
        result = '\n'
        for attr in sorted(self.__dict__):
            result += f'\t{attr} = {self.__dict__[attr]}\n'
        return result

    def __str__(self):
        return f'<Instance of {self.__class__.__name__}, address {id(self)}: {self.__attrnames()}>'


if __name__ == '__main__':
    import class_testmixin
    class_testmixin.tester(ListInstance)