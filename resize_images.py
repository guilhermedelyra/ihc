from PIL import Image
import glob

basewidth = 140
hsize = 120
diretorios = ['mouse', 'teclado', 'placa de video', 'monitor']

for filename in glob.iglob('***/**/*_index_g.jpg', recursive=True):
	img = Image.open(filename)
	img = img.resize((basewidth, hsize), Image.ANTIALIAS)
	aux = filename.split('/')
	out = '/'.join(aux[:-1]) + '/chamada_' + aux[-1]
	img.save(out) 