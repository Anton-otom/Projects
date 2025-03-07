import re


TEXT_DATA = """'Указ Президента РФ от 16 августа 2004 г. N 1082 "Вопросы Министерства обороны Российской\n'
             '03.02.2024 Система ГАРАНТ 1\n'
             'Указ Президента РФ от 16 августа 2004 г. N 1082 "Вопросы Министерства обороны Российской Федерации" (с изменениями и дополнениями)\n'
             'С изменениями и дополнениями от:\n'
             'С изменениями и дополнениями от:\n'
             '3, 5 сентября 2005 г., 15 апреля 2006 г., 7 мая, 27 июня, 9 ноября 2007 г., 29 июля, 23 октября, 17\n'
             'ноября 2008 г., 19 мая, 1 сентября 2009 г., 14 мая, 6 июля, 26 августа, 27 декабря 2010 г., 2\n'
             'января, 8, 19 апреля, 7 июня, 8, 26 июля, 10 августа, 22 ноября 2011 г., 29 февраля, 12 июля, 24\n'
             'декабря 2012 г., 29 июня, 23 июля, 21 декабря 2013 г., 27 января, 13 февраля, 12 июня, 28\n'
             'октября 2014 г., 3, 20 января, 16 июня, 31 декабря 2015 г., 1 апреля, 20 сентября, 30 ноября, 7\n'
             'декабря 2016 г., 27 марта, 1 июня, 17 августа, 10 сентября, 5 октября, 14, 20 ноября, 27 декабря\n'
             '2017 г., 9 февраля, 30 июля, 24, 25 октября, 27 декабря 2018 г., 1, 26 января, 8 июля, 2 августа\n'
             '2019 г., 5 июня, 23 июля, 6 октября, 5, 30 ноября, 21 декабря 2020 г., 5 марта, 26 июля, 31\n'
             'декабря 2021 г., 17 января, 5 марта, 4 мая 2022 г., 31 июля 2023 г.\n'
             '1. Утвердить прилагаемое Положение о Министерстве обороны Российской Федерации.\n'
             'Информация об изменениях: Пункт 2 изменен с 8 июля 2019 г. - Указ Президента России от 8 июля\n'
             '2019 г. N 324\n'
             'См. предыдущую редакцию\n'
             '2. Разрешить иметь в Министерстве обороны Российской Федерации двенадцать заместителей\n'
             'Министра, в том числе двух первых заместителей Министра, одного статс-секретаря - заместителя\n'
             'Министра, одного заместителя Министра - начальника Главного военно-политического управления\n'
             'Вооруженных Сил Российской Федерации и одного заместителя Министра - руководителя Аппарата Министра.\n'
             'Информация об изменениях: Пункт 3 изменен с 9 февраля 2018 г. - Указ Президента РФ от 9\n'
             'февраля 2018 г. N 60\n'
             'См. предыдущую редакцию\n'
             '3. Установить предельную численность центрального аппарата Министерства обороны\n'
             'Российской Федерации в количестве 10 740 единиц (без персонала по охране и обслуживанию зданий), в\n'
             'том числе федеральных государственных гражданских служащих в количестве 4930 человек.\n'
             '4. Правительству Российской Федерации:\n'
             'в 3-месячный срок привести свои акты в соответствие с настоящим Указом, а также представить\n'
             'предложения по приведению актов Президента Российской Федерации в соответствие с настоящим\n'
             'Указом;\n'
             'обеспечить финансирование расходов, связанных с реализацией настоящего Указа.\n'
             '5. Министру обороны Российской Федерации в 3-месячный срок:\n'
             'осуществить мероприятия, направленные на реализацию настоящего Указа;\n'
             'представить в пределах установленной компетенции предложения о приведении актов\n'
             'Президента Российской Федерации в соответствие с настоящим Указом.\n'
             '6. Признать утратившими силу:\n'
             'Указ Президента Российской Федерации от 11 ноября 1998 г. N 1357 "Вопросы Министерства\n'
             'обороны Российской Федерации и Генерального штаба Вооруженных Сил Российской Федерации"\n'
             '(Собрание законодательства Российской Федерации, 1998, N 46, ст. 5652);\n'
             'Указ Президента Российской Федерации от 25 марта 2000 г. N 573 "О внесении изменений в\n'
             'Положение о Министерстве обороны Российской Федерации, утвержденное Указом Президента\n'
             'Российской Федерации от 11 ноября 1998 г. N 1357 "Вопросы Министерства обороны Российской\n'
             'Федерации и Генерального штаба Вооруженных Сил Российской Федерации" (Собрание\n'
             'законодательства Российской Федерации, 2000, N 13, ст. 1343);\n'
             'Указ Президента Российской Федерации от 6 июля 2002 г. N 693 "О внесении дополнения в\n'
             'Положение о Министерстве обороны Российской Федерации, утвержденное Указом Президента\n'
             'Российской Федерации от 11 ноября 1998 г. N 1357 "Вопросы Министерства обороны Российской\n'
             'Федерации и Генерального штаба Вооруженных Сил Российской Федерации" (Собрание\n'
             'законодательства Российской Федерации, 2002, N 27, ст. 2681);\n'
             'Указ Президента Российской Федерации от 5 августа 2002 г. N 845 "О внесении изменения в\n'
             'Положение о Министерстве обороны Российской Федерации, утвержденное Указом Президента\n'
             'Российской Федерации от 11 ноября 1998 г. N 1357 "Вопросы Министерства обороны Российской\n'
             'Указ Президента РФ от 16 августа 2004 г. N 1082 "Вопросы Министерства обороны Российской\n'
             '03.02.2024 Система ГАРАНТ 2\n'
             'Федерации и Генерального штаба Вооруженных Сил Российской Федерации" (Собрание\n'
             'законодательства Российской Федерации, 2002, N 32, ст. 3164);\n'
             'пункт 4 Указа Президента Российской Федерации от 21 июля 2003 г. N 793 "Вопросы\n'
             'организации альтернативной гражданской службы" (Собрание законодательства Российской Федерации,\n'
             '2003, N 30, ст. 3044);\n'
             'пункт 5 Указа Президента Российской Федерации от 21 июля 2003 г. N 821 "О военном\n'
             'геральдическом знаке - эмблеме и флаге Министерства обороны Российской Федерации" (Собрание\n'
             'законодательства Российской Федерации, 2003, N 32, ст. 3169);\n'
             'Указ Президента Российской Федерации от 10 сентября 2003 г. N 1058 "Вопросы Министерства\n'
             'обороны Российской Федерации и Генерального штаба Вооруженных Сил Российской Федерации"\n'
             '(Собрание законодательства Российской Федерации, 2003, N 37, ст. 3574);\n'
             'пункт 25 приложения N 1 к Указу Президента Российской Федерации от 19 ноября 2003 г. N\n'
             '1365 "Об изменении и признании утратившими силу некоторых актов Президента РСФСР и Президента\n'
             'Российской Федерации в связи с совершенствованием государственного управления в области\n'
             'безопасности Российской Федерации" (Собрание законодательства Российской Федерации, 2003, N 47,\n'
             'ст. 4520).\n'
             '7. Настоящий Указ вступает в силу со дня его подписания.\n'
             'Президент Российской Федерации В. Путин\n'
             'Москва, Кремль\n'
             '16 августа 2004 года\n'
             'N 1082 '"""


def TEXT_DATA_re_one_string(TEXT_DATA):
    TEXT_DATA_re = re.findall(r'[A-zА-я0-9\ .,()";:-]+', TEXT_DATA)
    TEXT_DATA_re_in_one = ''
    for line in TEXT_DATA_re:
        TEXT_DATA_re_in_one += line
    TEXT_DATA_re_in_one = re.sub(r'\d\d.\d\d.\d\d\d\d Система ГАРАНТ \d', '', TEXT_DATA_re_in_one)
    TEXT_DATA_re_in_one = re.sub(r' {2,}', ' NEW_STRING ', TEXT_DATA_re_in_one)
    TEXT_DATA_re_in_one = re.sub(r' NEW_STRING ', '\n', TEXT_DATA_re_in_one)
    return TEXT_DATA_re_in_one


if __name__ == '__main__':
    print(TEXT_DATA_re_one_string(TEXT_DATA))
