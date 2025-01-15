import pdfminer.high_level

with open('docs/Положение о Минобороны.pdf', 'rb') as file:
    file1 = open(r'pdf_to_text.txt', 'a+')
    pdfminer.high_level.extract_text_to_fp(file, file1)
    file1.close()

file_from_prf = open('pdf_to_text.txt', 'r')
for string in file_from_prf:
    string = string.split()
    print(string)
file_from_prf.close()