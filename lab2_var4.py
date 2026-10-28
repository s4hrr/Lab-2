from csv import reader
from random import randint
import xml.dom.minidom as minidom


def read_books():
    with open('books.csv', 'r', encoding='windows-1251') as csvfile:
        table = list(reader(csvfile, delimiter=';'))
    return table[1:]


def count_long_titles(books):
    count = 0
    for row in books:
        if len(row[1]) > 30:
            count += 1
    return count


def search_author(books, search_line):
    flag = 0
    for row in books:
        if search_line.lower() in row[3].lower() and float(row[7]) < 200:
            print(f'{row[3]}. {row[1]} - {row[7]} руб.')
            flag += 1
    if flag == 0:
        print('Ничего не найдено.')
    else:
        print(f'Найдено {flag} результатов.')


def make_refs(books):
    output = open('references.txt', 'w', encoding='utf-8')
    for i in range(1, 21):
        row = books[randint(0, len(books) - 1)]
        year = row[6].split(' ')[0].split('.')[2]
        output.write(f'{i}. {row[3]}. {row[1]} - {year}\n')
    output.close()


def read_currency():
    xml_file = open('currency.xml', 'r', encoding='windows-1251')
    dom = minidom.parseString(xml_file.read().encode('windows-1251'))
    xml_file.close()
    codes = {}
    for node in dom.getElementsByTagName('Valute'):
        num_code = node.getElementsByTagName('NumCode')[0].firstChild.data
        char_code = node.getElementsByTagName('CharCode')[0].firstChild.data
        codes[int(num_code)] = char_code
    return codes


def all_tags(books):
    tags = []
    for row in books:
        for tag in row[12].split('#'):
            tag = tag.strip()
            if tag != '' and tag not in tags:
                tags.append(tag)
    return tags


def top_books(books):
    sorted_books = sorted(books, key=lambda row: int(row[8]), reverse=True)
    for i in range(20):
        row = sorted_books[i]
        print(f'{i + 1}. {row[1]} ({row[3]}), выдач: {row[8]}')


books = read_books()
print(f'Названий длиннее 30 символов: {count_long_titles(books)}')

while True:
    search_line = input('Введите автора (0 - выход): ')
    if search_line == '0':
        break
    search_author(books, search_line)

make_refs(books)
print(read_currency())

tags = all_tags(books)
print(f'Всего тегов: {len(tags)}')
print(tags)
top_books(books)
