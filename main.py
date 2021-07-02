# %%
"""
Find all authors from publications of certain organization
from file dowloaded from Scopus.
"""
import pandas as pd
from collections import Counter
import re

FILE = 'scopus (4).csv'
ORGANIZATION = 'Physical-Chemical Medicine' 
RESULT_FILE = 'resultFCM_x.txt'
AUTHORS_NUMBERS = True
frame = pd.read_csv(FILE, encoding='utf8')
authors = []
for rec in frame['Авторы организаций']:
    for auth_rec in rec.split(';'):
        if ORGANIZATION in auth_rec:
            lastn, inits, *trash = auth_rec.split(',')
            authors.append(f'{lastn} {inits}')
if not AUTHORS_NUMBERS:
    authors = ', '.join(set(authors))
else:
    auth_nums = Counter(authors).most_common()
    authors = [f'{auth}({num})' for auth, num in auth_nums]
    authors = ', '.join(authors)
authors = re.sub(r'\s+', ' ', authors).strip()
with open(RESULT_FILE, 'w', encoding='utf') as f:
    f.write(authors)

# %%
