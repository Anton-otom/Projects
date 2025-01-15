import spacy
import random
#import docx
import re
import locale
import spacy_Text_Data

from spacy.tokens import Doc
from spacy.training import Example
#для работы nlp.create_optimizer()
from spacy.language import Language
#для загрузки результатов предыдущих обучений нейросети
from spacy.pipeline import EntityRecognizer

#для лучшего распознавания русского языка в самом коде
locale.setlocale(locale.LC_ALL, 'ru_RU.utf-8')

# Цвета для вывода
class bcolors:
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    UND = '\033[4m' #Нижнее подчёркивание
    BOLD = '\033[1m'#Нижнее жирное подчёркивание
    CYAN = '\033[96m'


nlp = spacy.load("ru_core_news_lg")
doc = nlp(spacy_Text_Data.TEXT_DATA_re_one_string(spacy_Text_Data.TEXT_DATA))


a = "До обучения:"
print(f"{bcolors.CYAN}{a: ^100}{bcolors.ENDC}")
name_a = 'сущность'
for i, ent in enumerate(doc.ents):
    print(f"{i + 1} {name_a: <8}: ent.text: {ent.text: <25} | ent.lemma_: {ent.lemma_: <25} | ent.label_: {ent.label_: <25}")

LABEL = "BOSS"
TRAINING_DATA = [
    ("Указ Президента РФ от 16 августа 2004 г. N 1082 'Вопросы Министерства обороны Российской Федерации' (с изменениями и дополнениями)", [(57, 77, "Boss")]),
    ("Указ Президента РФ от 16 августа 2004 г. N 1082 'Вопросы Министерства обороны Российской Федерации'", [(57, 77, "Boss")]),
    ("1. Утвердить прилагаемое Положение о Министерстве обороны Российской Федерации.", [(37, 57, "Boss")]),
    ("2. Разрешить иметь в Министерстве обороны Российской Федерации двенадцать заместителей", [(21, 41, "Boss")]),
    ("3. Установить предельную численность центрального аппарата Министерства обороны", [(59, 79, "Boss")]),
    ("Указ Президента Российской Федерации от 11 ноября 1998 г. N 1357 'Вопросы Министерства обороны Российской Федерации и Генерального штаба Вооруженных Сил Российской Федерации'", [(74, 94, "Boss")]),
    ('Указ Президента Российской Федерации от 25 марта 2000 г. N 573 "О внесении изменений вПоложение о Министерстве обороны Российской Федерации', [(98, 118, "Boss")]),
    ('утвержденное Указом Президента Российской Федерации от 11 ноября 1998 г. N 1357 "Вопросы Министерства обороны Российской Федерации и Генерального штаба Вооруженных Сил Российской Федерации"', [(89, 109, "Boss")]),
    ('О внесении изменения в Положение о Министерстве обороны Российской Федерации', [(35, 55, "Boss")]),
    ('от 16 августа 2004 г. N 1082 "Вопросы Министерства обороны Российской Федерации и Генерального штаба Вооруженных Сил Российской Федерации"', [(38, 58, "Boss")]),
    ('"О военном геральдическом знаке - эмблеме и флаге Министерства обороны Российской Федерации" (Собрание законодательства Российской Федерации, 2003, N 32, ст. 3169)', [(50, 70, "Boss")]),
    ("Нам нужно быть в Фести к 19:00.", []),
    ("Я люблю красные яблоки.", []),
    ("Фести работает с 10:00 до 19:00.", []),
    ("В магазине продают бананы.", []),
    ("В Фести делают вкусные пирожные.", []),
    ("Фести работает без перерыва.", []),
    ("В округе много кофеен: Старс, Кофемания, Фести к 19:00.", [])
]

#ner = nlp.get_pipe('ner')
#ner.add_label(LABEL)

optimizer = nlp.create_optimizer()

disabled_pipes = []

#Отключение необучаемых компонетов конвейера
for pipe_name in nlp.pipe_names:
    if pipe_name != 'ner':
        nlp.disable_pipe(pipe_name)
        disabled_pipes.append(pipe_name)

for i in range(50):
    random.shuffle(TRAINING_DATA)
    for text, entity_offsets in TRAINING_DATA:
        text = nlp.make_doc(text)
        example = Example.from_dict(text, {"entities": entity_offsets})
        nlp.update([example], sgd=optimizer)

#Подключение отключенных компонетов конвейера
for pipe_name in disabled_pipes:
    nlp.enable_pipe(pipe_name)

ner = nlp.get_pipe('ner')
ner.to_disk('Mark_1')

doc = nlp(spacy_Text_Data.TEXT_DATA_re_one_string(spacy_Text_Data.TEXT_DATA))

print('_'*100, '\n')
b = "Обучение проведено!"
print(f'{bcolors.OKGREEN}{b: ^100}{bcolors.ENDC}')
print('_'*100, '\n')

c = "После обучения:"
print(f"{bcolors.YELLOW}{c: ^100}{bcolors.ENDC}")
for i, ent in enumerate(doc.ents):
    print(f"{i + 1} {name_a: <8}: ent.text: {ent.text: <25} | ent.lemma_: {ent.lemma_: <25} | ent.label_: {ent.label_: <25}")
