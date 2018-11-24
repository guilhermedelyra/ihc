import urllib.request
from bs4 import BeautifulSoup
import requests
import random
import re
import bleach
import os
f = open('test.html').read()
soup = BeautifulSoup(f)

# pega infos do produto e salva

de = re.escape('Caracterí')
ate = re.escape('(bruto com embalagem)')
patt = r'(?<=' + de + r')(.*?)(?=' + ate + r')'
kek = bleach.clean(str(soup), tags=[], attributes={}, styles=[], strip=True)
# print(kek)
rgx = re.compile(patt, re.DOTALL)
get_caracteristicas = rgx.findall(kek)[0].split('ticas:')[-1]
dirty_caracteristicas = bleach.clean(get_caracteristicas, tags=[], attributes={}, styles=[], strip=True)
caracteristicas = dirty_caracteristicas.replace('Especificações:', '\nEspecificações:\n').replace('- ', '\n- ').replace('\n\n', '\n').replace('  ', ' ').replace(' -', '\n- ').replace('\n\n', '\n').replace('  ', ' ').replace('\n\n\n', '\n').replace('\n \n', '\n').strip() + '\n'

print (caracteristicas)