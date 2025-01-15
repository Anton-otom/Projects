import pymorphy2

morph = pymorphy2.MorphAnalyzer()
OVY_name = 'МИНИСТЕРСТВА ОБОРОНЫ'
OVY_name = OVY_name.split(' ')
# padegi = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
cases = {'nomn': ['OVY_name_nomn', ''], # Именительный
          'gent': ['OVY_name_gent', ''], # Родительный
          'datv': ['OVY_name_datv', ''], # Дательный
          'accs': ['OVY_name_accs', ''], # Винительный
          'ablt': ['OVY_name_ablt', ''], # Творительный
          'loct': ['OVY_name_loct', '']} # Предложный
for key in cases:
    for word in OVY_name:
        refactor = morph.parse(word)[0]
        pad = refactor.inflect({key})
        if cases[key][1]:
            cases[key][1] += ' ' + pad.word
        else:
            cases[key][1] += pad.word.title()
    print(cases[key][1])
# _______________________________________________________________________________________________________________________

# # Определение ОВУ
# ovy_name = None
# # Преобразование слова в родительный падеж
# morph = pymorphy2.MorphAnalyzer()
# ovy_name = ovy_name[0].split(' ')
# ovy_name_gent = ''
# for word in ovy_name:
#     refactor_word = morph.parse(word)[0]
#     case = refactor_word.inflect({'gent'})
#     if ovy_name_gent:
#         ovy_name_gent += ' ' + case.word
#     else:
#         ovy_name_gent += case.word.title()
# # ovy_name = f'{bcolors.CYAN}{ovy_name_gent}{bcolors.ENDC}'
# ovy_name = ovy_name_gent