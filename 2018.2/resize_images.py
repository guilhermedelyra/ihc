from PIL import Image
import glob

basewidth = 150
hsize = 120

for filename in glob.iglob('.data/**/*_index_g.jpg', recursive=True):
	img = Image.open(filename)
	img = img.resize((basewidth, hsize), Image.ANTIALIAS)
	img = img.crop((0, 0, basewidth, hsize+100))
	aux = filename.split('/')
	out = '/'.join(aux[:-1]) + '/_chamada_' + aux[-1].split('.jpg')[0] + '.png'
	img.save(out, 'PNG') 