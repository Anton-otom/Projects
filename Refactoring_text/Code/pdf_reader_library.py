"""
install PyMuPDFb (для python от версии 3.8(3.10))
install PyMuPDF

Только PDF-a. В документе на 35 стр. ошибок распознавания не нашёл.
"""
import fitz
import re

pdf_file = ["Положение о Минобороны.pdf",
    "ПМО 2016 г. № 260дсп Положение о ГК СВ.pdf"]

pdf_path = "docs/" + pdf_file[0]
text = ''
file = fitz.open(pdf_path)
for pageNum, page in enumerate(file.pages()):
    text += page.get_text()

# Создаётся строковая переменная из всех данных
result = text.replace('\n', ' ')
# Удаляются лишние пробелы
result = re.sub(r' {2,}', ' ', result)
# Удаление номеров страниц
result = re.sub(r'( [0-9]{1,3} )', ' ', result)
# print(result)
# print('-' * 80)

# Разбивка строки на смысловые абзацы
result = re.sub(r'(?<=[а-яА-Я.,:;)]) (?=([0-9]{1,2}[.)])([0-9]{1,2}\))?[^(\d{2}.\d{2}.\d{4})])', r'\n', result)
result = re.sub(r'(?<=[:;]) (?=[а-яА-Я])', r'\n-', result)
result = re.sub(r'(?<=[а-яА-Я]) (?=\*)', r'\n', result)
result = re.sub(r'(?<=[а-яА-Я]) (?=\(?[вВ] ред.)', r'\n', result)
result = re.sub(r'(Список изменяющих документов)(\n)', r'\n\1 ', result)
result = re.sub(r'(Утверждено) ', r'\1\n', result)
result = re.sub(r' (I+V+\.) ', r'\n\1', result)
result = re.sub(r'(\w-) ', r'\1', result)

# Преобразование строки в список
# list_ = result.split('\n')
# for el in list_:
#     print(el)

# Сохранение распознанного текста в файле
# file_ = open('result28.03.txt', 'w')
# for tekst in result:
#     file_.writelines(tekst)
# file_.close()

#_______________________________________________________________________________________________________________________
"""
PDF-a распознаётся с небольшим процентом критических ошибок (проверены только текстовые объекты).
Некоторые слова после распознавания подставляются на своё место в тексте.
"""
import re
# Для считывания PDF
import PyPDF2
# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTLayoutContainer, LTChar, LTRect, LTFigure, LTTextContainer
# Для извлечения текста из таблиц в PDF
import pdfplumber
# Для извлечения изображений из PDF
from PIL import Image
from pdf2image import convert_from_path
# Для выполнения OCR, чтобы извлекать тексты из изображений
import pytesseract
# Для удаления дополнительно созданных файлов
import os


# Функция для извлечения текста
def text_extraction(element):
    # Текст из вложенного текстового элемента
    line_text = element.get_text()
    # Список со всеми форматами, встречающимися в строке текста
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Обработка каждого символа в строке текста
            for character in text_line:
                if isinstance(character, LTChar):
                    # Название шрифта символа
                    line_formats.append(character.fontname)
                    # Размер шрифта символа
                    line_formats.append(character.size)
    # Уникальные размеры и названия шрифтов в строке
    format_per_line = list(set(line_formats))
    # Кортеж с текстом в каждой строке вместе с его форматом
    return (line_text, format_per_line)


# Функция для вырезания элементов изображений из PDF
def crop_image(element, pageObj):
    # Координаты для вырезания изображения из PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0, element.y0, element.x1, element.y1]
    # Обрезка страницы по координатам (left, bottom, right, top)
    pageObj.mediabox.lower_left = (image_left, image_bottom)
    pageObj.mediabox.upper_right = (image_right, image_top)
    # Сохранение обрезанной страницы в новый PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(pageObj)
    # Сохранение обрезанного PDF в новый файл
    with open('cropped_image.pdf', 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)


# # Функция для преобразования PDF в изображения
def convert_to_images(input_file,):
    images = convert_from_path(input_file)
    image = images[0]
    output_file = "PDF_image.png"
    image.save(output_file, "PNG")


# # Функция для считывания текста из изображений
# def image_to_text(image_path):
#     # Считывается изображение
#     img = Image.open(image_path)
#     # Извлекается текст из изображения
#     text = pytesseract.image_to_string(img)
#     return text


# Извлечение таблиц из страницы
# def extract_table(pdf_path, page_num, table_num):
#     # Открытие файла pdf
#     pdf = pdfplumber.open(pdf_path)
#     # Определение исследуемой страницы
#     table_page = pdf.pages[page_num]
#     # Извлечение соответствующей таблицу
#     table = table_page.extract_tables()[table_num]
#     return table


# Преобразование таблицы в соответствующий формат
def table_converter(table):
    table_string = ''
    # Проход по каждой строке в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        # Удаление разрывов строки из текста с переносом
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else]
        # Преобразуем таблицу в строку
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
        # Удаляем последний разрыв строки
    table_string = table_string[:-1]
    return table_string


pdf_file = "Приказ Министр обороны Российской Федерации от 16.10.2018 № 580 (в редакции от 27.01.2024 № 41).pdf"
pdf_path = "docs/" + pdf_file
pdfFileObj = open(pdf_path, 'rb')
# Объект считывателя PDF
pdfReaded = PyPDF2.PdfReader(pdfFileObj)
# Словарь для извлечения текста из каждого изображения
text_per_page = {}
# Извлечение страниц из PDF
for pagenum, page in enumerate(extract_pages(pdf_path)):
    # Переменные, необходимые для извлечения текста со страницы
    pageObj = pdfReaded.pages[pagenum]
    text_parameters = []
    page_text = []
    line_format = []
    text_from_images = []
    page_content = []
    # Количество исследованных таблиц
    table_num = 0
    first_element = True
    table_extraction_flag = False
    # Открытие файла pdf
    pdf = pdfplumber.open(pdf_path)
    # Определение исследуемой страницы
    page_tables = pdf.pages[pagenum]
    # Количество таблиц на странице
    tables = page_tables.find_tables()
    # Все элементы
    page_elements = [(element.y1, element) for element in page._objs]
    # Сортировка всех элементов по порядку нахождения на странице
    page_elements.sort(key=lambda a: a[0], reverse=True)

    #Поиск элементов, составляющих страницу
    for i, component in enumerate(page_elements):
        # Положение верхнего края элемента в PDF
        pos = component[0]
        # Извлечение элемента структуры страницы
        element = component[1]

        # Проверка, является ли элемент текстовым
        if isinstance(element, LTTextContainer):
            # Проверка, находится ли текст в таблице
            if table_extraction_flag == False:
                # Функция извлечения текста и формата для каждого текстового объекта
                (line_text, format_per_line) = text_extraction(element)
                # Добавление текста каждой строки к тексту страницы
                page_text.append(line_text)
                # Добавление формата каждой строки, содержащей текст
                line_format.append(format_per_line)
                page_content.append(line_text)
            else:
                # Пропуск текста, находящегося в таблице
                pass

        # # Проверка элементов на наличие изображений
        if isinstance(element, LTFigure):
            # Вырезание изображения из PDF
            crop_image(element, pageObj)
            # Преобразование обрезанного pdf в изображение
            convert_to_images('cropped_image.pdf')
            # Извлечение текста из изображения
            image_text = image_to_text('PDF_image.png')
            text_from_images.append(image_text)
            page_content.append(image_text)
            # Добавление условного обозначения в списки текста и формата
            page_text.append('image')
            line_format.append('image')

    # Создание ключа для словаря
    dctkey = 'Page_' + str(pagenum + 1)
    # Добавление списка списков как значение ключа страницы
    text_per_page[dctkey] = [page_text, line_format, text_from_images, page_content]

pdfFileObj.close()
# Удаление созданных дополнительных файлов
os.remove('cropped_image.pdf')
os.remove('PDF_image.png')
# Удаление содержимого страницы
result = ''.join(text_per_page['Page_1'][3])
print(result)
#_____________________________________________________________________________________________________________
"""
Преобразовывает PDF-a в TXT и считывает текст.

Не распознаются символы переноса текста.
"""

import pdfminer.high_level

with open('docs/Положение о Минобороны.pdf', 'rb') as file:
    file1 = open(r'pdf_to_text.txt', 'a+')
    pdfminer.high_level.extract_text_to_fp(file, file1)
    file1.close()

file_from_prf = open('pdf_to_text.txt', 'r')
for string in file_from_prf:
    print(string)
file_from_prf.close()
#____________________________________________________________________________________________________
"""
install opencv_python

Не тестировалось
"""
import cv2
import pytesseract
from pdf2image import convert_from_path

#Конвертация в jpeg
pages = convert_from_path('name.pdf', 100)
pages[0].save('out.jpg', 'JPEG')

# Считывается изображения и переводится в другую цветовую градацию
imgcv = cv2.imread('out.jpg')
imgcv = cv2.cvtColor(imgcv, cv2.COLOR_BGR2RGB)
#Преобразование в текст и вывод
print(pytesseract.image_to_string(imgcv, lang='rus'))
#________________________________________________________________________________________________
"""
#install wand
#install PyOCR
#install tesseract-ocr
#install Pil

Не тестировалось
"""
from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

#Дескриптор распознавания текста (tesseract) и язык, используемый pyocr
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[1]

#Списки для хранения изображений и текста
req_image = []
final_text = []

#Открытие PDF и преобразование в jpeg
image_pdf = Image(filename="./PDF_FILE_NAME", resolution=300)
image_jpeg = image_pdf.convert('jpeg')

#Image преобразовал отдельные страницы PDF в отдельные двоичные объекты изображения
#Перебираем в цикле и добавляем в виде большого двоичного объекта в список req_image.
for img in image_jpeg.seqence:
    img_page = Image(image=img)
    req_image.append(img_page.make_blob('jpeg'))

#Распознавание больших двоичных объектов изображения
for img in req_image:
    txt = tool.image_to_string(PI.open(io.BytesIO(img)), lang=lang, builder=pyocr.builders.TextBuilder())
    final_text.append(txt)
# ________________________________________________________________________________________________
# Задание и дополнение нумерации функций
Duties_f = []
# Счетчик номера функции
count_f = 1
# Счетчик срабатывания добавления функции в "Duties_f", кроме одной и той же подфункции
count_uf = 1
# Счетчик номера подфункции
count_pf = 0
# Счетчик номера выявленного текста функции
count_ppf = 1
# Счетчик уровня вложенности функции
count_deep = 1
duti_f = []
duti_pf = []
duti_ppf = []
for match in re.finditer(r'(?P<Duti_f>[0-9]+\)\s(?P<Duti_f_not_number>.*:))|'
                         # r'(?P<Duti_pfl>(?P<Duti_pf_letter>[а-я])\).*:)+|'
                         r'(?P<Duti_pf>-?.*:)+|'
                         # r'(?P<Duti_ppfl>(?P<Duti_ppf_letter>[а-я])\).*[:;.])+'
                         r'(?P<Duti_ppf>-?.*[;.])+', moduls_doc['Функции']):
    # Поиск функций
    if match["Duti_f"]:
        count_deep = 1
        duti_f = ['Функция', count_f, count_ppf, ovy_name, match["Duti_f_not_number"][:-1]]
        # Все print() в теле цикла позволяют вывести функции по уровням вложенности
        print(f'{duti_f[0]} {duti_f[1]} {duti_f[3]} {duti_f[4]}')
        print(f'count_deep - {count_deep}')
        count_f += 1
        count_uf = 1
        count_pf = 0
        count_ppf = 1
    # Поиск подфункций
    elif match["Duti_pf"]:
    # elif match["Duti_pf"] or match["Duti_pfl"]:
        count_deep = 2
        # if match["Duti_pfl"]:
        #     duti_pf = [count_f - 1, match["Duti_pf_letter"], match["Duti_pfl"][1:]]
        # else:
        #     duti_pf = [count_f - 1, count_uf, match["Duti_pf"][1:]]
        duti_pf = [count_f - 1, count_uf, match["Duti_pf"][1:-1]]
        print(f'\t{duti_pf[0]}_{duti_pf[1]} {duti_pf[2]}')
        print(f'\tcount_deep - {count_deep}')
        count_uf += 1
        count_pf += 1
        count_ppf = 1
    # Поиск текста функций
    elif match["Duti_ppf"]:
    # elif match["Duti_ppf"] or match["Duti_ppfl"]:
        # Если была выявлена подфункция
        if duti_pf:
            # Если счётчик функции в подфункции равен счётчику функции - 1 (счётчик функции идёт на опережение на 1)
            if duti_pf[0] == count_f - 1:
                duti_ppf = ['Функция', count_f - 1, count_uf - 1, count_ppf, ovy_name, duti_f[4], duti_pf[2], match["Duti_ppf"][1:]]
                Duties_f.append(['Функция', count_f - 1, count_uf - 1, count_ppf, ovy_name, duti_f[4], duti_pf[2], match["Duti_ppf"][1:]])
                # if match["Duti_ppfl"]:
                #     duti_ppf[3] = match["Duti_ppf_letter"]
                print(f'\t\t{count_f - 1}_{count_uf - 1}_{duti_ppf[3]} {match["Duti_ppf"][1:]}')
                if count_ppf == 1:
                    count_deep = 3
                print(f'\t\tcount_deep - {count_deep}')
                count_ppf += 1
            else:
                Duties_f.append(['Функция', count_f - 1, count_uf, ovy_name, duti_f[4], match["Duti_ppf"][1:]])
                print(f'\t{count_f - 1}_{count_uf} {match["Duti_ppf"][1:]}')
                if count_uf == 1:
                    count_deep = 2
                print(f'\tcount_deep - {count_deep}')
                count_uf += 1
                count_ppf += 1
        else:
            # Добавление функции в виде списоков в итоговую переменную
            Duties_f.append(['Функция', count_f - 1, count_uf, ovy_name, duti_f[4], match["Duti_ppf"][1:]])
            print(f'\t{count_f - 1}_{count_uf} {match["Duti_ppf"][1:]}')
            if count_uf == 1:
                count_deep = 2
            print(f'\tcount_deep - {count_deep}')
            count_uf += 1
            count_ppf += 1
# Замена значения по ключу 'Функции' на список списков
moduls_doc['Функции'] = Duties_f