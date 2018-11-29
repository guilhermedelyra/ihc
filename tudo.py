import urllib.request
from bs4 import BeautifulSoup
import random
import re
import bleach
import os
import requests

def create_dir(directory):
	if not os.path.exists('Jojogos/lib/etc/product_data/product-images/'+directory):
		os.makedirs('Jojogos/lib/etc/product_data/product-images/'+directory)

def return_soup(link):
	r = requests.get(link)
	html = r.text
	soup = BeautifulSoup(html, "lxml")

	if (not soup.title):
		soup = return_soup(link)

	return soup

def strip_html(src, allowed=['strong', 'br']):
	return bleach.clean(src, tags=allowed, strip=True, strip_comments=True)

def file_name(string):
	string = string.replace(' ', '_')
	string = ''.join(e for e in string if e.isalnum() or e == '_')
	return string

def get_products(soup):
	div_products = soup.find_all("div", {"class": "listagem-img"})
	products = []
	for div in div_products:
		ahrefs = div.find_all("a", href=True)
		for url in ahrefs:
			products.append(url['href']);

	# get 15 random products in all products
	random_products = random.sample(range(len(products)), 2)
	products = [products[i] for i in random_products]

	return products

def make_product_dir(soup):
	name = soup.title.string.split('KaBuM! - ')[-1]
	name = file_name(name)
	dirname = p+'/'+name
	create_dir(dirname)

	return dirname

def get_images(soup, dirname):
	ul_slideshow = soup.find_all("ul", {"class":"slides","id":"imagem-slide"})[0]
	lis = ul_slideshow.find_all("li")
	imgs = []
	for li in lis:
		for img in li.find_all("img", src=True):
			imgs.append(img['src'])

	# save images
	for img in imgs:
		filename = 'Jojogos/lib/etc/product_data/product-images/'+dirname+'/'+file_name(img.split('/')[-1].split('.jpg')[0])+'.jpg'
		urllib.request.urlretrieve(img, filename)

	return

def get_price(soup, original, alternative):
	orig_price = str(soup.find("div", {"class":original})).split('R$')[-1]
	alt_price = str(soup.find("div", {"class":alternative})).split('R$')[-1]
	price = orig_price if alt_price == 'None' else alt_price
	price = bleach.clean(price, tags=[], attributes={}, styles=[], strip=True).strip().replace(',', '.')

	if (price != 'None' and price):
		aux = price.split('por')[0].strip().split('.')
		price = ''.join(aux[:-1])+'.'+aux[-1]
		return price
	else:
		return None

def get_specs(soup, dirname):
	_from = re.escape('Caracterí')
	_until = re.escape('(bruto com embalagem)')
	patt = r'(?<=' + _from + r')(.*?)(?=' + _until + r')'
	rgx = re.compile(patt, re.DOTALL)

	# clean_soup = bleach.clean(str(soup), tags=[], attributes={}, styles=[], strip=True)

	get_specs = rgx.findall(strip_html(str(soup)))[0].split('ticas:')[-1].replace('<br/>\n<br/>', '<br/>')
	specs = get_specs.replace('Especificações:', '\nEspecificações:\n').replace('- ', '\n- ').replace('\n\n', '\n').replace('  ', ' ').replace(' -', '\n- ').replace('\n\n', '\n').replace('  ', ' ').replace('\n\n\n', '\n').replace('\n \n', '\n').strip() + '\n'

	# pega preço antigo, atual e promoção boleto
	normal_price = get_price(soup, "preco_normal", "preco_desconto-cm")
	old_price = get_price(soup, "preco_antigo", "preco_antigo-cm")

	prices = ""

	if (old_price != None):
		prices += "\nPreço antigo: R$%s" % old_price

	prices += "\nPreço normal: R$%s" % normal_price
	discount_price = float(normal_price) - float(normal_price) * 0.15
	prices += "\nPreço boleto: R${:.2f}".format(discount_price)

	specs = specs.replace('\n', '<br>').replace('<br><br>', '<br>') + prices

	f = open('Jojogos/lib/etc/product_data/product-images/'+dirname+'/'+'specs.txt', 'w')
	f.write(specs)

	return

create_dir('')

# search x category in KaBuM
# 'Cadeiras', 'Computadores', 'Disco Rigido', 'Games', 'Headsets', 'Memoria Ram', 'Mesa', 'Monitores', 'Mouses', 
searches = ['Mousepad', 'Notebook', 'Pen Drive', 'Placa de Video', 'Processador', 'Smartphone', 'SSD', 'Teclado']

for p in searches:
	soup = return_soup("https://www.kabum.com.br/cgi-local/site/listagem/listagem.cgi?string=%s&btnG=" % p)
	p = file_name(p)
	create_dir(p)

	products = get_products(soup)

	for url_p in products:
		soup = return_soup(url_p)

		# pega name do produto e cria pasta
		print(url_p, soup.title)
		dirname = make_product_dir(soup)
		get_images(soup, dirname)
		get_specs(soup, dirname)
