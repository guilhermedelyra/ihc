from PIL import Image
import glob
import cv2
basewidth = 140
hsize = 120
diretorios = ['mouse', 'teclado', 'placa de video', 'monitor']

for filename in glob.iglob('***/**/test_chamada_*.jpg', recursive=True):
	img = cv2.imread(filename, cv2.IMREAD_COLOR)
	# img = img.crop((0, 0, basewidth, hsize+80))

	font = cv2.FONT_ITALIC
	cv2.putText(img, 'Preço haha', (15, 150), font, 0.5, (200, 200, 200), 1, cv2.LINE_AA)
	aux = filename.split('/')
	out = '/'.join(aux[:-1]) + '/test_' + aux[-1]
	cv2.imwrite(out, img)