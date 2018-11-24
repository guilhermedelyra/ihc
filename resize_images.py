from PIL import Image
import glob

basewidth = 140
hsize = 120

for filename in glob.iglob('***/**/*_index_g.jpg', recursive=True):
	img = Image.open(filename)
	img = img.resize((basewidth, hsize), Image.ANTIALIAS)
	img = img.crop((0, 0, basewidth, hsize+60))
	aux = filename.split('/')
	out = '/'.join(aux[:-1]) + '/chamada_' + aux[-1].split('.jpg')[0] + '.png'
	img.save(out, 'PNG') 