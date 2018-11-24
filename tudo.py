import urllib.request
from bs4 import BeautifulSoup
import requests
import random
import re
import bleach
import os


def cria_dir(directory):
	if not os.path.exists('.data/'+directory):
		os.makedirs('.data/'+directory)

def return_soup(link):
	r = requests.get(link)
	html = r.text
	soup = BeautifulSoup(html, "lxml")
	return soup

def file_name(string):
	string = string.replace(' ', '_')
	string = ''.join(e for e in string if e.isalnum() or e == '_')
	return string

cria_dir('')

# procura x categoria na kabum
procuras = ['placa de video', 'processador']#,'headset', 'monitor', 'mouse', 'teclado']
for p in procuras:

	soup = return_soup("https://www.kabum.com.br/cgi-local/site/listagem/listagem.cgi?string=%s&btnG=" % p)
	p = file_name(p)
	cria_dir(p)

	# pega K produtos da categoria procurada
	div_produtos = soup.find_all("div", {"class": "listagem-img"})
	produtos = []
	for div in div_produtos:
		ahrefs = div.find_all("a", href=True)
		for url in ahrefs:
			produtos.append(url['href']);

	random_products = random.sample(range(len(produtos)), 5)
	produtos = [produtos[i] for i in random_products]
	
	for url_p in produtos:
		soup = return_soup(url_p)
		
		# pega nome do produto e cria pasta
		nome = soup.title.string.split('KaBuM! - ')[-1]
		nome = file_name(nome)
		dirname = p+'/'+nome
		cria_dir(dirname)

		# pega array de slideshow
		ul_slideshow = soup.find_all("ul", {"class":"slides","id":"imagem-slide"})[0]
		lis = ul_slideshow.find_all("li")
		imgs = []
		for li in lis:
			for img in li.find_all("img", src=True):
				imgs.append(img['src'])

		# salva as imagens
		for img in imgs:
			filename = '.data/'+dirname+'/'+file_name(img.split('/')[-1].split('.jpg')[0])+'.jpg'
			urllib.request.urlretrieve(img, filename)

		# pega infos do produto e salva
		de = re.escape('Caracterí')
		ate = re.escape('(bruto com embalagem)')
		patt = r'(?<=' + de + r')(.*?)(?=' + ate + r')'
		rgx = re.compile(patt, re.DOTALL)

		clean_soup = bleach.clean(str(soup), tags=[], attributes={}, styles=[], strip=True)
		get_caracteristicas = rgx.findall(clean_soup)[0].split('ticas:')[-1]
		caracteristicas = get_caracteristicas.replace('Especificações:', '\nEspecificações:\n').replace('- ', '\n- ').replace('\n\n', '\n').replace('  ', ' ').replace(' -', '\n- ').replace('\n\n', '\n').replace('  ', ' ').replace('\n\n\n', '\n').replace('\n \n', '\n').strip() + '\n'

		# pega preço antigo, atual e promoção boleto
		preco_normal = bleach.clean(str(soup.find("div", {"class":"preco_normal"})).split('R$')[-1], tags=[], attributes={}, styles=[], strip=True).strip().replace(',', '.')
		preco_antigo = bleach.clean(str(soup.find("div", {"class":"preco_antigo"})).split('R$')[-1], tags=[], attributes={}, styles=[], strip=True).strip().replace(',', '.')
		if (preco_normal == 'None'):
			preco_normal = bleach.clean(str(soup.find("div", {"class":"preco_desconto-cm"})).split('R$')[-1], tags=[], attributes={}, styles=[], strip=True).strip().replace(',', '.')
		if (preco_antigo == 'None'):
			preco_antigo = bleach.clean(str(soup.find("div", {"class":"preco_antigo-cm"})).split('R$')[-1], tags=[], attributes={}, styles=[], strip=True).strip().replace(',', '.')

		aux = preco_normal.split('.')
		preco_normal = ''.join(aux[:-1])+'.'+aux[-1]
		print(preco_normal)
		print(preco_antigo, ' ', type(preco_antigo))
		prices = ""

		if (preco_antigo != 'None' and preco_antigo):
			aux = preco_antigo.split('por')[0].strip().split('.')
			preco_antigo = ''.join(aux[:-1])+'.'+aux[-1]
			prices += "\nPreço antigo: R$%s" % preco_antigo

		prices += "\nPreço normal: R$%s" % preco_normal
		boleto = float(preco_normal) - float(preco_normal) * 0.15
		prices += "\nPreço boleto: R${:.2f}".format(boleto)

		caracteristicas += prices

		f = open('.data/'+dirname+'/'+'specs.txt', 'w')
		f.write(caracteristicas)
