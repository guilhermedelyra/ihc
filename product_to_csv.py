import glob
import re
from pandas import DataFrame
import json

table = {
	'SKU':[],
	'Name':[],
	'Description':[],
	'Cost Price':[],
	'Old Price':[],
	'Price':[],
	'Available On':[],
	'Stock':[],
	'Height':[],
	'Width':[],
	'Depth':[],
	'Weight':[],
	'Position':[],
	'Taxonomies':[],
	'Permalink':[],
	'image_variant1':[],
	'image_variant2':[],
	'image_variant3':[],
	'image_variant4':[],
	'image_variant5':[],
	'image_variant6':[],
	'image_variant7':[],
	'image_variant8':[],
	'image_variant9':[],
	'image_variant10':[],
	'image_variant11':[],
	'image_variant12':[],
	'image_variant13':[],
	'image_variant14':[],
	'image_variant15':[],
	'image_variant16':[],
	'image_variant17':[],
	'image_variant18':[],
	'image_variant19':[],
	'image_variant20':[],
	'image_variant21':[],
	'image_variant22':[],
	'image_variant23':[],
	'image_variant24':[],
	'image_variant25':[],
	'image_variant26':[]
}


sku = 0

pat_norm = re.escape('Preço normal: R$')
pat_old = re.escape('Preço antigo: R$')
pat_discount = re.escape('Preço boleto: R$')

rgx_norm = re.compile(r'[\n\r].*' + pat_norm + r'\s*([^\n\r]*)')
rgx_old = re.compile(r'[\n\r].*' + pat_old + r'\s*([^\n\r]*)')
rgx_discount = re.compile(r'[\n\r].*' + pat_discount + r'\s*([^\n\r]*)')

for filename in glob.iglob('Jojogos/lib/etc/product_data/product-images/***/**/specs.txt', recursive=True):
	category = filename.split('/')[-3].title().replace('_', ' ')
	product_path = filename.split('/')[-2]
	product_name = filename.split('/')[-2].replace('_', ' ')

	file = open(filename).read()
	specs = file.split('Preço ')[0]

	norm_price = rgx_norm.findall(file)[0]
	old_price = rgx_old.findall(file)[0] if rgx_old.findall(file) else ''
	discount_price = rgx_discount.findall(file)[0]

	table['SKU'].append(sku)
	table['Name'].append(product_name)
	table['Description'].append(specs)
	table['Cost Price'].append(discount_price)
	table['Old Price'].append(old_price)
	table['Price'].append(norm_price)
	table['Available On'].append('')
	table['Stock'].append('')
	table['Height'].append('')
	table['Width'].append('')
	table['Depth'].append('')
	table['Weight'].append('')
	table['Position'].append('')
	table['Taxonomies'].append('Categories > '+category)
	table['Permalink'].append('')

	product_image = list(glob.iglob('Jojogos/lib/etc/product_data/product-images/***/%s/*_index_g.jpg' % product_path, recursive=True))[0]
	image_path_to_csv = '/'.join(product_image.split('/')[-3:])
	table['image_variant2'].append(image_path_to_csv)
	i = 1
	for imgs in glob.iglob('Jojogos/lib/etc/product_data/product-images/***/%s/*.jpg' % product_path, recursive=True):
		img_path = '/'.join(imgs.split('/')[-3:])
		if (img_path != image_path_to_csv):
			sti = str(i)
			key = 'image_variant'+sti
			i += 1 if i != 1 else 2
			table[key].append(img_path)

	for j in range(i, 27):
		if (j != 2):
			key = 'image_variant'+str(j)
			table[key].append('')

	sku+=1

for i in table:
	print(i, len(table[i]))

df = DataFrame(table, columns= list(table.keys()))
df.to_csv (r'xd.csv', index = None, header=True, sep=';') #Don't forget to add '.csv' at the end of the path
