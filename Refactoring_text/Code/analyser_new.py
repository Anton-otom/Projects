# -*- coding: cp1251 -*-
import locale
import os
import re
from datetime import datetime

import pymorphy3

import spacy
from pdfminer.high_level import extract_text

# import MainApp
# from ISKP_new.settings import BASE_DIR
# from MainApp.models import *

locale.setlocale(locale.LC_ALL, 'ru_RU.utf-8')


################################### =ПЕРЕМЕННЫЕ= ###################################
# Первые две переменные нужны для того, что избежать повторного вызова функций
# Загружен ли документ
file_uploaded = False
# Проверен ли документ (выделены ли основные поля)
chckd = False

# Счетчик обязанностей
duties_counter = 0
# Массив названий ОВУ. Заполняется из базы
db_array = []
# Полное название ОВУ, к которому относится документ
boss_ovu_fullname = None
# Тип участника (ОВУ, ЦОВУ, ЗМО, етц.)
mem_type_id = None
# Объект ОВУ, к которому относится документ, из бд
dut_ovu_boss = None
# Тип объекта ОВУ, к которому относится документ
dut_ovu_boss_type = None
# Объект ЗМО/МО/етц., к которому относится документ, из бд
dut_dl_boss = None
# Название НПА
fname = None
# Тип НПА из названия
doc_type_duty = None
# Подписной номер НПА
fnumber = None
# Дата вступления в силу НПА
fdate = None
# Актуальность НПА
factual = None
# Уровень НПА
flevel = None
# Вид НПА
fdtype = None

# Название используемой модели, дефолт: ru_core_news_lg
model = "C:\\Users\\Хоперия\\Desktop\\test_new\\ISKP_new\\ISKP_new\\model_prod"
# Список объектов-сущностей, которые будут выводиться при тестировании
entities = ['BOSS', 'PZMO', 'ZMO', 'COVU', 'OVU', 'FS']

# Длинна строк, которые будут пропускаться при тестировании файла
skip_chars = 20

# Массив обязанностей из PDF
array_duties = []
array_duties_count = 0
# Ответственный ОВУ из PDF
document_OVU_name = ""
# загрузка обученной nlp-модели
nlp = spacy.load(model)

###################################################################################


# Функция тестирования НПА в виде PDF файла
def run_test_PDF(text: str):
    global duties_counter, array_duties_count, array_duties, document_OVU_name
    duties_counter = 0
    array_duties = []
    array_duties_count = 0
    if text:
        text = re.sub("Статья\s+\d.+\n", "", text)
        trace = open("text.log", "w")
        trace.write("text: " + repr(text) + "\n________________________________________\n")
        trace.close()
        # Пытаемся определить к какому ОВУ относится данный НПА
        text_header = text[0:1400].replace("\n", " ").replace("  ", " ")
        document_OVU_name = re.search(r'(?i)(((?<=Вопросы\s)|(?<=Об\sутверждении\sПоложения\s(о\s|об)))(.*?)(?=Российской\sФедерации|["»]))', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=Утвердить\sобязанности\s)(.*?)(?=\()', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=Утвердить\sприлагаемые\sобязанности\s)(.*?)(?=\s\()', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=Утвердить\sприлагаемое\sПоложение\s(о\s|об))(.*?)(?=\.)', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=Положение\s(о\s|об))(.*?)(?=Российской\sФедерации|\()', text_header)

        # Пропускаем I главу документа (общие положения)
        text = re.sub("П.\s*Основные", "II. Основные", text)
        text = get_text_after(r'\WII\.', text)
        # Отсекаем формы в конце документа
        text = text.split("(форма)")[0]
        text = text.split("Типовая форма")[0]
        text = re.split("Приложение\s*(№|N)\s*1\s*к\s*", text)[0]
        # Для приказов, в которых есть перечень изменений. Убрать всё, что до предложения со словом П Е Р Е Ч Е Н Ь
        text = get_text_after(r'П\sЕ\sР\sЕ\sЧ\sЕ\sН\sЬ[\d\D]*?(1\.|:)', text)

        # Убираем мусорные выражения во всём тексте
        text = re.sub("Документ\sпредоставлен\sКонсультантПлюс\s(www\.consultant\.ru\s)*Дата\sсохранения:\s\d{1,2}\.\d{1,2}\.\d{4}","", text)
        text = re.sub("Федеральный\sзакон\sот\s\d{2}\.\d{2}\.\d{4}.{2,15}", "", text)
        text = re.sub("Постановление\sПравительства\sРФ\sот\s\d{2}\.\d{2}\.\d{4}\sN\s\d{1,4}", "", text)
        text = re.sub("\(ред\.\sот\s\d{2}\.\d{2}\.\d{4}\)\s\".{5,100}\"", "", text)
        text = re.sub("КонсультантПлюс", "", text)
        text = re.sub("надежная\sправовая\sподдержка", "", text)
        text = re.sub("www\.consultant\.ru","", text)
        text = re.sub("Страница\s", "", text)
        text = re.sub("\d{1,3}\sиз\s\d{1,3}", "", text)
        text = re.sub("«Приложение[\d\D]*?РЕШЕНИЕ:", "", text)

        # Убираем мусорные символы во всём тексте(2)
        text = text.replace("<\*>", "")
        text = text.replace("__", "")
        text = text.replace("--", "")
        text = text.replace("\n\n", "\n")

        # Убираем мусорные выражения во всём тексте (3)
        text = re.sub("П\s?Р\s?И\s?К\s?А\s?З[\d\D]*?от[\d\D]*?№\s*\d{1,3}\s", "", text)
        text = re.sub("П\s?Р\s?И\s?К\s?А\s?З[\d\D]*?П\s?Р\s?И\s?К\s?А\s?З\s?Ы\s?В\s?А\s?Ю", "", text)
        text = re.sub("МИНИСТР ОБОРОНЫ[\d\D]*?Шойгу", "", text)
        text = re.sub("ВРЕМЕННО ИСПОЛНЯЮЩИЙ[\d\D]+", "", text)
        text = re.sub("НАЧАЛЬНИК[\d\D]+", "", text)
        text = re.sub("\s+МИНИСТР\s+ОБОРОНЫ\s+р\s+о\s+с\s+с\s+и\s+й\s+с\s+к\s+о\s+й\s+ф\s+е\s+д\s+е\s+р\s+а\s+ц\s+и\s+и\s+", "", text)

        # Разбиение текста построчно на обязанности
        paragraphs = re.split("\n(?=\d{1,2}\.)|"
                              "\n(?=\w{1,2}\))|"
                              "(?<=;)\s\n|"
                              "(?<=:)\s\n|"
                              "(?<=;)\n|"
                              "(?<=:)\n|"
                              "(?<=\.)\s\n", text)
        #
        # trace = open("analyser.log", "w")
        # trace.write("document_OVU_name: " + str(document_OVU_name) + "\n")
        # trace.close()

        # Функция получения Головного органа, его типа, Головного ДЛ
        get_OVU_fields()

        # Текущий тип обязанностей (задача, функция или полномочие).
        # Определять по вводному предложению, например: "II Основными задачами Министерства обороны является:"
        # После этого предложения идет перечисление задач.
        # При начале следующего пункта (пример: "III Функции министерства обороны...") тип обязанности меняется на соответствующий.
        duties_type_current = ""
        for paragraph in paragraphs:
            if paragraph:
                paragraph_len = len(paragraph)
                if paragraph_len >= skip_chars:
                    # Убираем лишние символы
                    paragraph = paragraph.replace("\n", " ").replace("  ", " ")
                    # Убираем мусорные выражения в отдельных предложениях
                    paragraph = re.sub("(\(.*ред\..+\))", "", paragraph)
                    paragraph = re.sub("(\(.*введен.+\))", "", paragraph)
                    paragraph = re.sub("(\(.*введена.+\))", "", paragraph)
                    search_type = re.search(r'(Основные\sзадачи.+|Основными\sзадачами.+|Функции.+|функции:|Руководство|ОБЯЗАННОСТИ|полномочия:|Предназначение\sи\sзадачи)', paragraph)
                    if (paragraph_len >= skip_chars) and not search_type:
                        paragraph = paragraph.strip()
                        doc8 = nlp(" (" + (re.sub("\xad\n*\s", "", document_OVU_name[0].strip()) if document_OVU_name else '') + "): " + paragraph)
                        array_duties.append([duties_type_current, str(doc8)])  # print_doc_entities(doc8, nlp)

                    # Выделяем вид "объекта-обязанности"
                    if search_type:
                        duty_type = search_type[0].lower()
                        # Выделение задач
                        if duty_type[:3] == "осн" or duty_type[:5] == "предн":
                            duties_type_current = "Задача"
                        # Выделение обязанностей
                        elif duty_type[:3] == "обя":
                            duties_type_current = "Обязанность"
                        # Выделение функций
                        elif duty_type[0] == "ф":
                            duties_type_current = "Функция"
                        # Выделение полномочий
                        else:  # elif duty_type[:3] == "рук" or duty_type[:3] == "пол":
                            duties_type_current = "Полномочие"

        # Если вдруг попался скан и из него нечего выделить, необходимо создать хотя бы одну форму
        array_duties_count = len(array_duties)
        if array_duties_count == 0:
            array_duties.append([" ", "Обязанности не найдены."])
            array_duties_count += 1


# # Функция вывода участников Полномочия
# def print_doc_entities(_doc: Doc):
#     morph = pymorphy3.MorphAnalyzer()
#     ent_list = []
#     if _doc.ents:
#         for _ent in _doc.ents:
#             text = ' '.join([morph.parse(text_word)[0].normal_form for text_word in _ent.text.lower().split()])
#             if _ent.label_ in entities:
#                 if text not in ent_list:
#                     ent_list.append(text)
#     print('_____________________________________________________________________________________________________________________________________________________________________________________________________________________________')
#     print(f"{_doc}")
#     print(f"Участники — {len(ent_list)}:")
#     trace = open("полномочия_trace.log", "a")
#     trace.write("Полномочие: " + str(_doc) + "\n")
#     trace.write("Участники: " + str(ent_list) + "\n")
#     trace.write("________________________________________________________________________________________________________________________________________________________________________________________________________\n")
#     trace.close()
#     # Перевод названия ОВУ в начальную форму и поиск соответствия в базе данных ОВУ (пока без базы данных)
#     max_sim_org = ""
#     for ent in ent_list:
#         max_sim = 0
#         doc1 = nlp(ent)
#         for org in db_array:
#             org_cut = re.sub("(\sРФ|\sВС|\sМО)", "", org)
#             doc2 = nlp(' '.join([morph.parse(orgs_word)[0].normal_form for orgs_word in org_cut.lower().split()]))
#             current_sim = doc1.similarity(doc2)
#             if current_sim > max_sim:
#                 max_sim = current_sim
#                 max_sim_org = org
#             if current_sim > 0.9:
#                 break
#         print(f"\"{ent} [{max_sim_org}] - {max_sim} \"")
""

# Функция получения Головного органа, его типа, Головного ДЛ
def get_OVU_fields():
    global boss_ovu_fullname, mem_type_id, dut_ovu_boss, dut_dl_boss, dut_ovu_boss_type
    # полное название ОВУ, к которой относится документ
    boss_ovu_fullname = get_boss_OVU()
    # Тип участника (ОВУ, ЦОВУ, ЗМО, етц.)
    mem_type_id = Members.objects.raw('SELECT mem_type_id, id FROM "MainApp_members" WHERE mem_name = %s limit 1', [boss_ovu_fullname])[0].mem_type_id
    # объект ОВУ, к которому относится документ, из бд
    dut_ovu_boss = Members.objects.get(mem_name=boss_ovu_fullname)
    dut_ovu_boss_type = dut_ovu_boss.mem_type_id
    # объект ЗМО/МО/етц., к которому относится документ, из бд
    dut_dl_boss = Members.objects.raw('SELECT id FROM "MainApp_members" WHERE id IN (SELECT mem_department_boss_id FROM "MainApp_members" WHERE mem_name = %s limit 1)',[boss_ovu_fullname])[0]


# Функция поиска ОВУ в бд, соответствующего ОВУ, определенной в тексте документа
def get_boss_OVU():
    morph = pymorphy3.MorphAnalyzer()

    # Перевод названия ОВУ в начальную форму и поиск соответствия в базе данных ОВУ
    if document_OVU_name:
        text = ' '.join([morph.parse(text_word)[0].normal_form for text_word in document_OVU_name[0].strip().lower().split()])
    else:
        # Значение по умолчанию
        text = "Министерство обороны Российской Федерации"
    ovu_from_file = nlp(text)

    max_sim_org = ""
    max_sim = 0
    for org in db_array:
        org_cut = re.sub("(\sРФ|\sВС|\sМО)", "", org)
        ovu_from_db = nlp(' '.join([morph.parse(orgs_word)[0].normal_form for orgs_word in org_cut.lower().split()]))
        current_sim = ovu_from_file.similarity(ovu_from_db)
        if current_sim > max_sim:
            max_sim = current_sim
            max_sim_org = org
        if current_sim > 0.9:
            break
    return max_sim_org


# Функция перевода даты из текстового формата (который используется в НПА) в формат datetime
def text_to_date(from_date: datetime):
    day = re.search(r'\d{1,2}\s', from_date)[0]
    month = re.search(r'\w{3,8}', from_date)[0].lower()
    year = re.search(r'\d\s?\d\s?\d\s?\d\s?', from_date)[0].replace(" ", "")

    if month == 'января':
        month = '01'
    elif month == 'февраля':
        month = '02'
    elif month == 'марта':
        month = '03'
    elif month == 'апреля':
        month = '04'
    elif month == 'мая':
        month = '05'
    elif month == 'июня':
        month = '06'
    elif month == 'июля':
        month = '07'
    elif month == 'августа':
        month = '08'
    elif month == 'сентября':
        month = '09'
    elif month == 'октября':
        month = '10'
    elif month == 'ноября':
        month = '11'
    else:
        month = '12'

    return datetime.strptime(f"{year}/{month}/{day}".strip(), '%Y/%m/%d')


# Функция чтения PDF документа после загрузки и нажатия "Начать распознавание"
# Здесь определяются основные свойства документа (название, тип, уровень и т.д.)
# В конце вызывается функция для выделения обязанностей и полномочий из текста документа
def read_pdf(file_name: str):
    path = os.path.join(BASE_DIR, 'file/file_from_form/', file_name)
    full_text = extract_text(path)  # извлечение текста с помощью pdfminer
    # if len(full_text) < 100:
    #     full_text = MainApp.ocr_pdf.extract_text(path)  # вызов методов OCR
    # Убираем "плохие" символы
    full_text = remove_uchars(full_text)
    #
    text = full_text[0:2500]
    global fname, fnumber, fdate, factual, flevel, fdtype, doc_type_duty
    if text:
        text = re.sub("(?<=\d)\s*\n\n", "    ", text)
        text = text.replace("\n", " ").replace("  ", " ")
        name = re.search(r'(?i)(?<=РОССИЙСКАЯ\sФЕДЕРАЦИЯ\sФЕДЕРАЛЬНЫЙ\sЗАКОН).+?(?=Принят)|'
                         r'ПЕРЕЧЕНЬ\s[^I]{1,250}(?=утвержденное)|'
                         r'(Положение\s+(о|об)|ПОЛОЖЕНИЕ).+?(?=,\s+утвержденное|I|\d\.|в ред|\(|Список)|'
                         r'(?<=Утвердить\s)(.*?)Российской\s+Федерации|'
                         r'ИНСТРУКЦИЯ\s[^I]{1,250}', text)

        if name:
            fname = name[0].replace(".", "").replace("Инструкцию", "Инструкция")
            fname = re.sub("\s*прилагаемое\s+", "", fname)
            fname = re.sub("\s+\(приложение.*", "", fname)
        else:
            fname = file_name[:-4]
        doc_type_duty = fname.split(' ')[0].lower()
        number = re.search(r'([№N]\s{0,3}[ЗбО\d]\s?([ЗбО\d]\s?){0,3}(дсп|-ФЗ)?)', text)
        trace = open("text2500.log", "w")
        trace.write("text2500: " + repr(text) + "\n")
        trace.close()
        if not number:
            number = re.search(r'([№N]\s{0,2}\d{1,4}\s?(дсп|-ФЗ)?)', file_name)
        if number:
            fnumber = parse_doc_number(number[0])
        else:
            fnumber = '0'

        dates = re.search(r'\d{1,2}\s+\w{3,8}\s+\d\s?\d\s?\d\s?\d\s?\s+г.|\d{1,2}\.\d{1,2}\.\d{4}', text)
        if dates:
            if len(dates[0]) > 10:
                fdate = text_to_date(dates[0])
            else:
                fdate = datetime.strptime(dates[0], '%d.%m.%Y')
        else:
            dates = re.search(r'(?<=от)\s{0,2}\d{1,2}[._]\d{1,2}[._]\d{4}', file_name)
            if dates:
                fdate = datetime.strptime(dates[0].strip(), '%d.%m.%Y')
            else:
                fdate = datetime.now()

        if dates and fdate > datetime.now():
            factual = "Проект"
        else:
            factual = "Действует"

        level = re.search(r'(?i)((?<=приказ)|(?<=Указ)|(?<=Постановление))\s.+?(РФ|Федерации)(?=\s)|(?<=-)ФЗ|начальника.+?(РФ|Федерации).+?(РФ|Федерации)', text)
        if level:
            level_low = level[0].lower()
            if level_low == 'федеральный конституционный закон':
                flevel = 1
            elif level_low == 'федеральный закон':
                flevel = 2
            elif level_low == 'президента рф':
                flevel = 3
            elif level_low == 'правительства рф':
                flevel = 4
            elif level_low == 'министра обороны':
                flevel = 5
            elif level_low == 'заместителя министра обороны':
                flevel = 7
            elif level_low == 'органа военного управления':
                flevel = 8
            elif level_low == 'федеральной службы':
                flevel = 9
            else:
                flevel = 6  # по умолчанию 'министерства обороны'
        else:
            flevel = 6  # по умолчанию 'министерства обороны'

        dtype = re.search(r'(?i)приказ|указ|Постановление|Федеральный\sзакон|закон|распоряжение|решение|директива|указание|конституция', text)
        if dtype:
            dtype_low = dtype[0].lower()
            if dtype_low == 'конституция':
                fdtype = 1
            elif dtype_low == 'закон':
                fdtype = 2
            elif dtype_low == 'указ':
                fdtype = 3
            elif dtype_low == 'постановление':
                fdtype = 4
            elif dtype_low == 'распоряжение':
                fdtype = 5
            elif dtype_low == 'решение':
                fdtype = 7
            elif dtype_low == 'директива':
                fdtype = 8
            elif dtype_low == 'указание':
                fdtype = 9
            else:
                fdtype = 6  # по умолчанию 'приказ'
        else:
            fdtype = 6  # по умолчанию 'приказ'

        # ___Выделение обязанностей из текста PDF______
        run_test_PDF(full_text)
        # _____________________________________________
#


# Выгружаем массив названий ОВУ в память для быстрого поиска при определении Главного ОВУ документа
def load_ovu_array():
    if len(db_array) == 0:
        for ovu in Members.objects.all():
            db_array.append(ovu.mem_name)


# Получить текст, который находится после определенного шаблона. Если шаблон не найден, возвращает текст без изменений
def get_text_after(pattern, text: str):
    match = re.search(pattern, text)

    if match:
        return match.string[match.end():]
    else:
        return text


# Обработка номера документа из PDF
def parse_doc_number(num: str):
    trace = open("parse_doc_number.log", "w")
    trace.write("parse_doc_number: " + repr(num) + "\n")
    trace.close()
    result = ''
    for c in num:
        # Варианты номера
        if c in ['№', 'N']:
            result += '№ '
        # Цифры после номера и приставка дсп ил - ФЗ
        elif c != ' ':
            # Если цифры в PDF определены как буквы из-за схожести, то заменить буквы на цифры
            if c == 'З':
                c = '3'
            elif c == 'б':
                c = '6'
            elif c == 'O':
                c = '0'
            result += c
    return result


def remove_uchars(full_text: str):
    full_text = re.sub("\xad\n*", "", full_text)
    full_text = full_text.replace("\u2217", "")
    full_text = full_text.replace("\xa1", "")
    full_text = full_text.replace("\u25a0", "")
    full_text = full_text.replace("\x0c", "\n")

    return full_text
