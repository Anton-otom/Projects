# Для считывания PDF
import PyPDF2
# Для анализа структуры PDF и извлечения текста
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
# Для извлечения текста из таблиц в PDF
import pdfplumber
# Для извлечения изображений из PDF
from PIL import Image
from pdf2image import convert_from_path
# Для выполнения OCR, чтобы извлекать тексты из изображений
import pytesseract
# Для удаления дополнительно созданных файлов
import os

for pagenum, page in enumerate(extract_pages(pdf_path)):
    # Итеративно обходим элементы, из которых состоит страница
    for element in page:
        # Проверяем, является ли элемент текстовым
        if isinstance(element, LTTextContainer):
            # Функция для извлечения текста из текстового блока
            pass
            # Функция для извлечения формата текста
            pass
        # Проверка элементов на наличие изображений
        if isinstance(element, LTFigure):
            # Функция для преобразования PDF в изображение
            pass
            # Функция для извлечения текста при помощи OCR
            pass
        # Проверка элементов на наличие таблиц
        if isinstance(element, LTRect):
            # Функция для извлечения таблицы
            pass
            # Функция для преобразования содержимого таблицы в строку
            pass


def text_extraction(element):
    line_text = element.get_text()
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    return (line_text, format_per_line)


