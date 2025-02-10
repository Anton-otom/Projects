import re
import pymorphy2

from django import template


register = template.Library()

# Создать экземпляр класса для анализа слов
morph = pymorphy2.MorphAnalyzer()
# Множество слов, подлежащих цензуре
SET_BAD_WORDS = {'негодяй', 'редиска'}
# Паттерн поиска слов в тексте.
# Найти слова, в которых первая буква в любом регистре, а остальные только в нижнем.
WORDS_PATTERN = re.compile(r'\b[А-Яа-яA-Za-z][а-яa-z]*\b')


# Фильтр-цензор текста. Если 'value' не текст, то выбросить исключение.
@register.filter()
def censor(value):
    if isinstance(value, str):
        # Слова для исправления{'плохое слово': 'исправленное слово'}
        word_to_replace = {}
        # Убирать дублирование слов, для уменьшения кол-ва приведения слов к нормальной форме.
        data = list(set(WORDS_PATTERN.findall(value)))
        for word in data:
            # Привести слова к нормальной форме
            normal_form = morph.parse(word)[0].normal_form
            # Если проверяемое слово плохое, закрыть все буквы '*', кроме первой, и добавить в словарь.
            if normal_form in SET_BAD_WORDS:
                new_word = word[0] + '*' * (len(word)-1)
                word_to_replace[word] = new_word
        # Если нашли плохие слова, провести замену в 'value'
        if word_to_replace:
            for word, replacement in word_to_replace.items():
                value = value.replace(word, replacement)
    else:
        raise ValueError('Фильтр censor применим только к типу данных "str".')
    return value
