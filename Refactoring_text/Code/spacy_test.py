import spacy
import random
import docx
import re
import locale

from spacy.vocab import Vocab
from datetime import datetime
from spacy.training import Example
from spacy.symbols import ORTH, LEMMA
from spacy.tokens import Doc
from spacy.language import Language
from spacy.pipeline import EntityRecognizer
from spacy.util import minibatch, compounding

# Цвета для вывода
class bcolors:
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'#WARN
    ENDC = '\033[0m'#Конец применения цвета
    UND = '\033[4m' #Нижнее подчёркивание
    BOLD = '\033[1m'#Нижнее жирное подчёркивание
    CYAN = '\033[96m'

nlp = spacy.load("ru_core_news_lg")
doc = nlp(u'В округе много кофеен: Старс, Кофемания, Фести к 19:00')


a = "До обучения:"
print(f"{bcolors.CYAN}{a: ^40}{bcolors.ENDC}")
for ent in doc.ents:
    print(f"ent.text: {ent.text: <10} ent.label_: {ent.label_: <10}")

LABEL = "Kafe"
TRAIN_DATA = [
    ("Нам нужно быть в Фести к 19:00.", [(17, 22, "Kafe")]),
    ("Я люблю красные яблоки.", []),
    ("Фести работает с 10:00 до 19:00.", [(0, 5, "Kafe")]),
    ("В магазине продают бананы.", []),
    ("В Фести делают вкусные пирожные.", [(2, 7, "Kafe")]),
    ("Фести работает без перерыва.", [(0, 5, "Kafe")]),
    ("В округе много кофеен: Старс, Кофемания, Фести к 19:00.", [(41, 46, "Kafe")])
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

for i in range(115):
    random.shuffle(TRAIN_DATA)
    for text, entity_offsets in TRAIN_DATA:
        text = nlp.make_doc(text)
        example = Example.from_dict(text, {"entities": entity_offsets})
        nlp.update([example], sgd=optimizer)

#Подключение отключенных компонетов конвейера
for pipe_name in disabled_pipes:
    nlp.enable_pipe(pipe_name)

ner = nlp.get_pipe('ner')
ner.to_disk('Mark_1')

doc = nlp(u'В округе много кофеен: Старс, Кофемания, Фести к 19:00')

print('_'*40, '\n')
b = "Обучение проведено!"
print(f'{bcolors.OKGREEN}{b: ^40}{bcolors.ENDC}')
print('_'*40, '\n')

c = "После обучения:"
print(f"{bcolors.YELLOW}{c: ^40}{bcolors.ENDC}")
for ent in doc.ents:
    print(f"ent.text: {ent.text: <10} ent.label_: {ent.label_: <10}")

