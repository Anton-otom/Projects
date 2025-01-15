import fitz

pdf_file = ["Положение о Минобороны.pdf"]

pdf_path = "docs/" + pdf_file[0]
text = ''
file = fitz.open(pdf_path)
for pageNum, page in enumerate(file.pages()):
    text += page.get_text()

print(text)