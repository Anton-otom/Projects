import requests
import lxml.html
from lxml import etree

html = requests.get('https://www.python.org/').content

tree = etree.parse('Welcome to Python.org.html', lxml.html.HTMLParser())

ul = tree.findall('/div/section/div[2]/div[1]/div/ul/li[1]/a')

for li in ul:
    a = li.find('a')
    print(a.text)
