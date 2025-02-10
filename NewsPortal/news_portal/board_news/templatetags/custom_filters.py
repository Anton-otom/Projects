import re
import pymorphy2

from django import template


register = template.Library()

morph = pymorphy2.MorphAnalyzer()
LIST_BAD_WORDS = {'негодяй', 'редиска'}
WORDS_PATTERN = re.compile(r'\b[А-Яа-яA-Za-z][а-яa-z]*\b')


@register.filter()
def censor(value):
    if isinstance(value, str):
        word_to_replace = {}
        data = list(set(WORDS_PATTERN.findall(value)))
        for word in data:
            normal_form = morph.parse(word)[0].normal_form
            if normal_form in LIST_BAD_WORDS:
                new_word = word[0] + '*' * (len(word)-1)
                word_to_replace[word] = new_word
        if word_to_replace:
            for word, replacement in word_to_replace.items():
                value = value.replace(word, replacement)
    else:
        raise ValueError('Фильтр censor применим только к типу данных "str".')
    return value
