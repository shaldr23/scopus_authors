# %%
"""
Find all authors from publications of certain organization
from file dowloaded from Scopus.
"""
import pandas as pd

FILE = 'scopus (4).csv'
ORGANIZATION = 'Physical-Chemical Medicine' 
RESULT_FILE = 'resultFCM.txt'
frame = pd.read_csv(FILE, encoding='utf8')
authors = []
for rec in frame['Авторы организаций']:
    for auth_rec in rec.split(';'):
        if ORGANIZATION in auth_rec:
            lastn, inits, *trash = auth_rec.split(',')
            authors.append(f'{lastn} {inits}')
authors = ', '.join(set(authors))
with open(RESULT_FILE, 'w', encoding='utf') as f:
    f.write(authors)

# %%
