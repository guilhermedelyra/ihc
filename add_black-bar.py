from PIL import Image
import glob
import cv2
basewidth = 140
hsize = 120

for filename in glob.iglob('***/**/chamada_*.jpg', recursive=True):
	img = Image.open(filename)
	img = img.crop((0, 0, basewidth, hsize+60))
	aux = filename.split('/')
	out = '/'.join(aux[:-1]) + '/test_' + aux[-1]
	img.save(out) 