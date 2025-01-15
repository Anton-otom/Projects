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


################################### =����������= ###################################
# ������ ��� ���������� ����� ��� ����, ��� �������� ���������� ������ �������
# �������� �� ��������
file_uploaded = False
# �������� �� �������� (�������� �� �������� ����)
chckd = False

# ������� ������������
duties_counter = 0
# ������ �������� ���. ����������� �� ����
db_array = []
# ������ �������� ���, � �������� ��������� ��������
boss_ovu_fullname = None
# ��� ��������� (���, ����, ���, ���.)
mem_type_id = None
# ������ ���, � �������� ��������� ��������, �� ��
dut_ovu_boss = None
# ��� ������� ���, � �������� ��������� ��������
dut_ovu_boss_type = None
# ������ ���/��/���., � �������� ��������� ��������, �� ��
dut_dl_boss = None
# �������� ���
fname = None
# ��� ��� �� ��������
doc_type_duty = None
# ��������� ����� ���
fnumber = None
# ���� ���������� � ���� ���
fdate = None
# ������������ ���
factual = None
# ������� ���
flevel = None
# ��� ���
fdtype = None

# �������� ������������ ������, ������: ru_core_news_lg
model = "C:\\Users\\�������\\Desktop\\test_new\\ISKP_new\\ISKP_new\\model_prod"
# ������ ��������-���������, ������� ����� ���������� ��� ������������
entities = ['BOSS', 'PZMO', 'ZMO', 'COVU', 'OVU', 'FS']

# ������ �����, ������� ����� ������������ ��� ������������ �����
skip_chars = 20

# ������ ������������ �� PDF
array_duties = []
array_duties_count = 0
# ������������� ��� �� PDF
document_OVU_name = ""
# �������� ��������� nlp-������
nlp = spacy.load(model)

###################################################################################


# ������� ������������ ��� � ���� PDF �����
def run_test_PDF(text: str):
    global duties_counter, array_duties_count, array_duties, document_OVU_name
    duties_counter = 0
    array_duties = []
    array_duties_count = 0
    if text:
        text = re.sub("������\s+\d.+\n", "", text)
        trace = open("text.log", "w")
        trace.write("text: " + repr(text) + "\n________________________________________\n")
        trace.close()
        # �������� ���������� � ������ ��� ��������� ������ ���
        text_header = text[0:1400].replace("\n", " ").replace("  ", " ")
        document_OVU_name = re.search(r'(?i)(((?<=�������\s)|(?<=��\s�����������\s���������\s(�\s|��)))(.*?)(?=����������\s���������|["�]))', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=���������\s�����������\s)(.*?)(?=\()', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=���������\s�����������\s�����������\s)(.*?)(?=\s\()', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=���������\s�����������\s���������\s(�\s|��))(.*?)(?=\.)', text_header)
        if not document_OVU_name:
            document_OVU_name = re.search(r'(?i)(?<=���������\s(�\s|��))(.*?)(?=����������\s���������|\()', text_header)

        # ���������� I ����� ��������� (����� ���������)
        text = re.sub("�.\s*��������", "II. ��������", text)
        text = get_text_after(r'\WII\.', text)
        # �������� ����� � ����� ���������
        text = text.split("(�����)")[0]
        text = text.split("������� �����")[0]
        text = re.split("����������\s*(�|N)\s*1\s*�\s*", text)[0]
        # ��� ��������, � ������� ���� �������� ���������. ������ ��, ��� �� ����������� �� ������ � � � � � � � �
        text = get_text_after(r'�\s�\s�\s�\s�\s�\s�\s�[\d\D]*?(1\.|:)', text)

        # ������� �������� ��������� �� ��� ������
        text = re.sub("��������\s������������\s���������������\s(www\.consultant\.ru\s)*����\s����������:\s\d{1,2}\.\d{1,2}\.\d{4}","", text)
        text = re.sub("�����������\s�����\s��\s\d{2}\.\d{2}\.\d{4}.{2,15}", "", text)
        text = re.sub("�������������\s�������������\s��\s��\s\d{2}\.\d{2}\.\d{4}\sN\s\d{1,4}", "", text)
        text = re.sub("\(���\.\s��\s\d{2}\.\d{2}\.\d{4}\)\s\".{5,100}\"", "", text)
        text = re.sub("���������������", "", text)
        text = re.sub("��������\s��������\s���������", "", text)
        text = re.sub("www\.consultant\.ru","", text)
        text = re.sub("��������\s", "", text)
        text = re.sub("\d{1,3}\s��\s\d{1,3}", "", text)
        text = re.sub("�����������[\d\D]*?�������:", "", text)

        # ������� �������� ������� �� ��� ������(2)
        text = text.replace("<\*>", "")
        text = text.replace("__", "")
        text = text.replace("--", "")
        text = text.replace("\n\n", "\n")

        # ������� �������� ��������� �� ��� ������ (3)
        text = re.sub("�\s?�\s?�\s?�\s?�\s?�[\d\D]*?��[\d\D]*?�\s*\d{1,3}\s", "", text)
        text = re.sub("�\s?�\s?�\s?�\s?�\s?�[\d\D]*?�\s?�\s?�\s?�\s?�\s?�\s?�\s?�\s?�\s?�", "", text)
        text = re.sub("������� �������[\d\D]*?�����", "", text)
        text = re.sub("�������� �����������[\d\D]+", "", text)
        text = re.sub("���������[\d\D]+", "", text)
        text = re.sub("\s+�������\s+�������\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+�\s+", "", text)

        # ��������� ������ ��������� �� �����������
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

        # ������� ��������� ��������� ������, ��� ����, ��������� ��
        get_OVU_fields()

        # ������� ��� ������������ (������, ������� ��� ����������).
        # ���������� �� �������� �����������, ��������: "II ��������� �������� ������������ ������� ��������:"
        # ����� ����� ����������� ���� ������������ �����.
        # ��� ������ ���������� ������ (������: "III ������� ������������ �������...") ��� ����������� �������� �� ���������������.
        duties_type_current = ""
        for paragraph in paragraphs:
            if paragraph:
                paragraph_len = len(paragraph)
                if paragraph_len >= skip_chars:
                    # ������� ������ �������
                    paragraph = paragraph.replace("\n", " ").replace("  ", " ")
                    # ������� �������� ��������� � ��������� ������������
                    paragraph = re.sub("(\(.*���\..+\))", "", paragraph)
                    paragraph = re.sub("(\(.*������.+\))", "", paragraph)
                    paragraph = re.sub("(\(.*�������.+\))", "", paragraph)
                    search_type = re.search(r'(��������\s������.+|���������\s��������.+|�������.+|�������:|�����������|�����������|����������:|��������������\s�\s������)', paragraph)
                    if (paragraph_len >= skip_chars) and not search_type:
                        paragraph = paragraph.strip()
                        doc8 = nlp(" (" + (re.sub("\xad\n*\s", "", document_OVU_name[0].strip()) if document_OVU_name else '') + "): " + paragraph)
                        array_duties.append([duties_type_current, str(doc8)])  # print_doc_entities(doc8, nlp)

                    # �������� ��� "�������-�����������"
                    if search_type:
                        duty_type = search_type[0].lower()
                        # ��������� �����
                        if duty_type[:3] == "���" or duty_type[:5] == "�����":
                            duties_type_current = "������"
                        # ��������� ������������
                        elif duty_type[:3] == "���":
                            duties_type_current = "�����������"
                        # ��������� �������
                        elif duty_type[0] == "�":
                            duties_type_current = "�������"
                        # ��������� ����������
                        else:  # elif duty_type[:3] == "���" or duty_type[:3] == "���":
                            duties_type_current = "����������"

        # ���� ����� ������� ���� � �� ���� ������ ��������, ���������� ������� ���� �� ���� �����
        array_duties_count = len(array_duties)
        if array_duties_count == 0:
            array_duties.append([" ", "����������� �� �������."])
            array_duties_count += 1


# # ������� ������ ���������� ����������
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
#     print(f"��������� � {len(ent_list)}:")
#     trace = open("����������_trace.log", "a")
#     trace.write("����������: " + str(_doc) + "\n")
#     trace.write("���������: " + str(ent_list) + "\n")
#     trace.write("________________________________________________________________________________________________________________________________________________________________________________________________________\n")
#     trace.close()
#     # ������� �������� ��� � ��������� ����� � ����� ������������ � ���� ������ ��� (���� ��� ���� ������)
#     max_sim_org = ""
#     for ent in ent_list:
#         max_sim = 0
#         doc1 = nlp(ent)
#         for org in db_array:
#             org_cut = re.sub("(\s��|\s��|\s��)", "", org)
#             doc2 = nlp(' '.join([morph.parse(orgs_word)[0].normal_form for orgs_word in org_cut.lower().split()]))
#             current_sim = doc1.similarity(doc2)
#             if current_sim > max_sim:
#                 max_sim = current_sim
#                 max_sim_org = org
#             if current_sim > 0.9:
#                 break
#         print(f"\"{ent} [{max_sim_org}] - {max_sim} \"")
""

# ������� ��������� ��������� ������, ��� ����, ��������� ��
def get_OVU_fields():
    global boss_ovu_fullname, mem_type_id, dut_ovu_boss, dut_dl_boss, dut_ovu_boss_type
    # ������ �������� ���, � ������� ��������� ��������
    boss_ovu_fullname = get_boss_OVU()
    # ��� ��������� (���, ����, ���, ���.)
    mem_type_id = Members.objects.raw('SELECT mem_type_id, id FROM "MainApp_members" WHERE mem_name = %s limit 1', [boss_ovu_fullname])[0].mem_type_id
    # ������ ���, � �������� ��������� ��������, �� ��
    dut_ovu_boss = Members.objects.get(mem_name=boss_ovu_fullname)
    dut_ovu_boss_type = dut_ovu_boss.mem_type_id
    # ������ ���/��/���., � �������� ��������� ��������, �� ��
    dut_dl_boss = Members.objects.raw('SELECT id FROM "MainApp_members" WHERE id IN (SELECT mem_department_boss_id FROM "MainApp_members" WHERE mem_name = %s limit 1)',[boss_ovu_fullname])[0]


# ������� ������ ��� � ��, ���������������� ���, ������������ � ������ ���������
def get_boss_OVU():
    morph = pymorphy3.MorphAnalyzer()

    # ������� �������� ��� � ��������� ����� � ����� ������������ � ���� ������ ���
    if document_OVU_name:
        text = ' '.join([morph.parse(text_word)[0].normal_form for text_word in document_OVU_name[0].strip().lower().split()])
    else:
        # �������� �� ���������
        text = "������������ ������� ���������� ���������"
    ovu_from_file = nlp(text)

    max_sim_org = ""
    max_sim = 0
    for org in db_array:
        org_cut = re.sub("(\s��|\s��|\s��)", "", org)
        ovu_from_db = nlp(' '.join([morph.parse(orgs_word)[0].normal_form for orgs_word in org_cut.lower().split()]))
        current_sim = ovu_from_file.similarity(ovu_from_db)
        if current_sim > max_sim:
            max_sim = current_sim
            max_sim_org = org
        if current_sim > 0.9:
            break
    return max_sim_org


# ������� �������� ���� �� ���������� ������� (������� ������������ � ���) � ������ datetime
def text_to_date(from_date: datetime):
    day = re.search(r'\d{1,2}\s', from_date)[0]
    month = re.search(r'\w{3,8}', from_date)[0].lower()
    year = re.search(r'\d\s?\d\s?\d\s?\d\s?', from_date)[0].replace(" ", "")

    if month == '������':
        month = '01'
    elif month == '�������':
        month = '02'
    elif month == '�����':
        month = '03'
    elif month == '������':
        month = '04'
    elif month == '���':
        month = '05'
    elif month == '����':
        month = '06'
    elif month == '����':
        month = '07'
    elif month == '�������':
        month = '08'
    elif month == '��������':
        month = '09'
    elif month == '�������':
        month = '10'
    elif month == '������':
        month = '11'
    else:
        month = '12'

    return datetime.strptime(f"{year}/{month}/{day}".strip(), '%Y/%m/%d')


# ������� ������ PDF ��������� ����� �������� � ������� "������ �������������"
# ����� ������������ �������� �������� ��������� (��������, ���, ������� � �.�.)
# � ����� ���������� ������� ��� ��������� ������������ � ���������� �� ������ ���������
def read_pdf(file_name: str):
    path = os.path.join(BASE_DIR, 'file/file_from_form/', file_name)
    full_text = extract_text(path)  # ���������� ������ � ������� pdfminer
    # if len(full_text) < 100:
    #     full_text = MainApp.ocr_pdf.extract_text(path)  # ����� ������� OCR
    # ������� "������" �������
    full_text = remove_uchars(full_text)
    #
    text = full_text[0:2500]
    global fname, fnumber, fdate, factual, flevel, fdtype, doc_type_duty
    if text:
        text = re.sub("(?<=\d)\s*\n\n", "    ", text)
        text = text.replace("\n", " ").replace("  ", " ")
        name = re.search(r'(?i)(?<=����������\s���������\s�����������\s�����).+?(?=������)|'
                         r'��������\s[^I]{1,250}(?=������������)|'
                         r'(���������\s+(�|��)|���������).+?(?=,\s+������������|I|\d\.|� ���|\(|������)|'
                         r'(?<=���������\s)(.*?)����������\s+���������|'
                         r'����������\s[^I]{1,250}', text)

        if name:
            fname = name[0].replace(".", "").replace("����������", "����������")
            fname = re.sub("\s*�����������\s+", "", fname)
            fname = re.sub("\s+\(����������.*", "", fname)
        else:
            fname = file_name[:-4]
        doc_type_duty = fname.split(' ')[0].lower()
        number = re.search(r'([�N]\s{0,3}[���\d]\s?([���\d]\s?){0,3}(���|-��)?)', text)
        trace = open("text2500.log", "w")
        trace.write("text2500: " + repr(text) + "\n")
        trace.close()
        if not number:
            number = re.search(r'([�N]\s{0,2}\d{1,4}\s?(���|-��)?)', file_name)
        if number:
            fnumber = parse_doc_number(number[0])
        else:
            fnumber = '0'

        dates = re.search(r'\d{1,2}\s+\w{3,8}\s+\d\s?\d\s?\d\s?\d\s?\s+�.|\d{1,2}\.\d{1,2}\.\d{4}', text)
        if dates:
            if len(dates[0]) > 10:
                fdate = text_to_date(dates[0])
            else:
                fdate = datetime.strptime(dates[0], '%d.%m.%Y')
        else:
            dates = re.search(r'(?<=��)\s{0,2}\d{1,2}[._]\d{1,2}[._]\d{4}', file_name)
            if dates:
                fdate = datetime.strptime(dates[0].strip(), '%d.%m.%Y')
            else:
                fdate = datetime.now()

        if dates and fdate > datetime.now():
            factual = "������"
        else:
            factual = "���������"

        level = re.search(r'(?i)((?<=������)|(?<=����)|(?<=�������������))\s.+?(��|���������)(?=\s)|(?<=-)��|����������.+?(��|���������).+?(��|���������)', text)
        if level:
            level_low = level[0].lower()
            if level_low == '����������� ��������������� �����':
                flevel = 1
            elif level_low == '����������� �����':
                flevel = 2
            elif level_low == '���������� ��':
                flevel = 3
            elif level_low == '������������� ��':
                flevel = 4
            elif level_low == '�������� �������':
                flevel = 5
            elif level_low == '����������� �������� �������':
                flevel = 7
            elif level_low == '������ �������� ����������':
                flevel = 8
            elif level_low == '����������� ������':
                flevel = 9
            else:
                flevel = 6  # �� ��������� '������������ �������'
        else:
            flevel = 6  # �� ��������� '������������ �������'

        dtype = re.search(r'(?i)������|����|�������������|�����������\s�����|�����|������������|�������|���������|��������|�����������', text)
        if dtype:
            dtype_low = dtype[0].lower()
            if dtype_low == '�����������':
                fdtype = 1
            elif dtype_low == '�����':
                fdtype = 2
            elif dtype_low == '����':
                fdtype = 3
            elif dtype_low == '�������������':
                fdtype = 4
            elif dtype_low == '������������':
                fdtype = 5
            elif dtype_low == '�������':
                fdtype = 7
            elif dtype_low == '���������':
                fdtype = 8
            elif dtype_low == '��������':
                fdtype = 9
            else:
                fdtype = 6  # �� ��������� '������'
        else:
            fdtype = 6  # �� ��������� '������'

        # ___��������� ������������ �� ������ PDF______
        run_test_PDF(full_text)
        # _____________________________________________
#


# ��������� ������ �������� ��� � ������ ��� �������� ������ ��� ����������� �������� ��� ���������
def load_ovu_array():
    if len(db_array) == 0:
        for ovu in Members.objects.all():
            db_array.append(ovu.mem_name)


# �������� �����, ������� ��������� ����� ������������� �������. ���� ������ �� ������, ���������� ����� ��� ���������
def get_text_after(pattern, text: str):
    match = re.search(pattern, text)

    if match:
        return match.string[match.end():]
    else:
        return text


# ��������� ������ ��������� �� PDF
def parse_doc_number(num: str):
    trace = open("parse_doc_number.log", "w")
    trace.write("parse_doc_number: " + repr(num) + "\n")
    trace.close()
    result = ''
    for c in num:
        # �������� ������
        if c in ['�', 'N']:
            result += '� '
        # ����� ����� ������ � ��������� ��� �� - ��
        elif c != ' ':
            # ���� ����� � PDF ���������� ��� ����� ��-�� ��������, �� �������� ����� �� �����
            if c == '�':
                c = '3'
            elif c == '�':
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
