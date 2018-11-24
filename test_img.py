from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import glob
import re

height = 0

rgx_pa = re.compile(r'[\n\r].*Preço antigo:\s*([^\n\r]*)')
rgx_pn = re.compile(r'[\n\r].*Preço normal:\s*([^\n\r]*)')
rgx_pb = re.compile(r'[\n\r].*Preço boleto:\s*([^\n\r]*)')

colors = {
	"azul" : (75, 136, 162),
	"laranja" : (196, 93, 0),
	"preto" : (0, 0, 0),
	"branco" : (211, 212, 217),
	"vermelho" : (187, 10, 33)
}

font_preco_antigo = ImageFont.truetype("fonts/ChakraPetch-Regular.ttf", 10)
font_preco_atual = ImageFont.truetype("fonts/ChakraPetch-Bold.ttf", 18)
font_nome = ImageFont.truetype("fonts/ChakraPetch-Regular.ttf", 12)
font_comprar = ImageFont.truetype("fonts/ChakraPetch-Bold.ttf", 13)
font_detalhes = ImageFont.truetype("fonts/ChakraPetch-Bold.ttf", 11)

def word_wrap_nome (draw, nome):
	lines = ['','','','','']
	it = 0
	words = nome.split(' ')
	height = 122
	for w in words:
		if (len(lines[it] + w) < 21):
			lines[it] += w+' '
		else:
			it += 1

	if(lines[2] != ''):
		lines[1] += '...'
		lines = lines[:2]

	for l in lines:
		if (l != ''):
			draw.text((15, height), l, colors['azul'], font=font_nome)
			height += 15

	return draw, height
	
for filename in glob.iglob('.data/**/_chamada_*.png', recursive=True):
	img = Image.open(filename)
	specs = open('/'.join(filename.split('/')[:-1])+'/specs.txt').read()
	pa, pn, pb = rgx_pa.findall(specs), rgx_pn.findall(specs), rgx_pb.findall(specs)
	nome = filename.split('/')[2].replace('_', ' ').replace('  ', ' ').strip()
	img = img.convert('RGB')
	draw = ImageDraw.Draw(img)
	pp = ''
	if (pa):
		pp = pa[0]
	else:
		pp = pn[0]

	draw, height = word_wrap_nome(draw, nome)

	draw.text((15, height+3),"De %s por" % pp, colors['branco'], font=font_preco_antigo)
	draw.text((15, height+12),"%s" % pb[0], colors['azul'], font=font_preco_atual)
	draw.text((15, height+35),"+ COMPRAR", colors['laranja'], font=font_comprar)
	draw.text((15, height+50),"+  DETALHES", colors['laranja'], font=font_detalhes)

	aux = filename.split('/')
	out = '/'.join(aux[:-1]) + '/_final_' + aux[-1]

	img.save(out, 'PNG')

# nome = maior que preço antigo
# preço antigo = menor texto
# preço atual = maior texto negrito
# botao comprar = nome+1 negrito
# botao detalhes = nome-1 negrito
