# %%
"""
Find all authors from publications of certain organization
from file dowloaded from Scopus.
"""
import pandas as pd
from collections import Counter
import re

FILE = 'scopus (18).csv'
ORGANIZATION = 'Burnasyan'
RESULT_FILE = 'result.txt'
AUTHORS_NUMBERS = True # Выводить ли имена с номерами публикаций (либо просто список имен) 
CORRECT_INITS = True  # корректировать инициалы (Makarov V. -> Makarov V.V., если в списке есть оба варианта)
AUTHORFILE = 'authlist.txt'  # файл, полученный при копировании раскрывающегося списка авторов в Scopus, для коррекции числа публикаций


def authordict_from_authorfile(file=AUTHORFILE):
    """
    Сделать из файла (полученного из раскрывающегося списка авторов в Scopus)
    словарик с именами и количеством статей
    """
    with open(file) as f:
        text = f.read()
    authdict = {}
    for record in text.split('\n\n'):
        found = re.search(r'(\w+),\s+(\S+)\n.+\((\d+)\)', record)
        if found:
            groups = found.groups()
            name = f'{groups[0]} {groups[1]}'
            authdict[name] = int(groups[2])
    return authdict


def make_authorstring(authors):
    """"
    Make string of authors from either Counter or list (set)
    """
    if type(authors) == Counter:
        authors = [f'{auth}({num})' for auth, num in authors.most_common()]
    return ', '.join(authors)


frame = pd.read_csv(FILE, encoding='utf8')
authors = []
for rec in frame['Авторы организаций']:
    for auth_rec in rec.split(';'):
        if ORGANIZATION in auth_rec:
            lastn, inits, *trash = auth_rec.split(',')
            author = f'{lastn} {inits}'
            author = re.sub(r'\s+', ' ', author).strip()
            authors.append(author)

authors = Counter(authors)
if AUTHORFILE:
    # Скорректировать количество публикаций в соотв. с файлом (может увеличиться)
    authordict = authordict_from_authorfile()
    for auth, num in authors.items():
        num_x = authordict.get(auth, 0)
        if num_x > num:
            authors[auth] = num_x

if CORRECT_INITS:
    for auth, num in authors.items():
        for auth_x, num_x in authors.items():
            if auth.startswith(auth_x) and len(auth) > len(auth_x):
                authors[auth] += authors[auth_x]
                authors[auth_x] = 0
    authors = {auth: num for auth, num in authors.items() if num != 0}
    authors = Counter(authors)

if not AUTHORS_NUMBERS:
    authors = set(authors)

authorstring = make_authorstring(authors)
with open(RESULT_FILE, 'w', encoding='utf') as f:
    f.write(authorstring)

# %%
