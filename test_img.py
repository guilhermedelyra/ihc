from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

colors = {
	"azul" : (75, 136, 162),
	"laranja" : (196, 93, 0),
	"preto" : (0, 0, 0),
	"branco" : (211, 212, 217),
	"vermelho" : (187, 10, 33)
}

img = Image.open("sample_in.jpg")
draw = ImageDraw.Draw(img)

antes = ImageFont.truetype("ChakraPetch-Regular.ttf", 10)
depois = ImageFont.truetype("ChakraPetch-Bold.ttf", 15)
draw.text((15, 142),"de: $100", colors['branco'], font=antes)
draw.text((15, 152),"por: $149", colors['azul'], font=depois)

img.save('sample-out.jpg')