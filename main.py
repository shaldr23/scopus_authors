# %%
"""
Find all authors from publications of certain organization
from file dowloaded from Scopus.
"""
import pandas as pd
from collections import Counter
import re

FILE = 'scopus (18).csv'
ORGANIZATION = 'Strategic Planning' 
RESULT_FILE = 'result_x.txt'
AUTHORS_NUMBERS = True
CORRECT_INITS = True  # корректировать инициалы (Makarov V. -> Makarov V.V., если в списке есть оба варианта)

frame = pd.read_csv(FILE, encoding='utf8')
authors = []
for rec in frame['Авторы организаций']:
    for auth_rec in rec.split(';'):
        if ORGANIZATION in auth_rec:
            lastn, inits, *trash = auth_rec.split(',')
            author = f'{lastn} {inits}'
            author = re.sub(r'\s+', ' ', author).strip()
            authors.append(author)
if CORRECT_INITS:
    auth_set = set(authors)
    for num, auth in enumerate(authors):
        for auth_s in auth_set:
            if auth_s.startswith(auth) and len(auth_s) > len(auth):
                authors[num] = auth_s
if not AUTHORS_NUMBERS:
    authors = ', '.join(set(authors))
else:
    auth_nums = Counter(authors).most_common()
    authors = [f'{auth}({num})' for auth, num in auth_nums]
    authors = ', '.join(authors)
with open(RESULT_FILE, 'w', encoding='utf') as f:
    f.write(authors)

# %%
