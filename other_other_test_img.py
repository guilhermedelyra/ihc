import os.path
import sys

from PIL import Image, ImageDraw, PILLOW_VERSION

if __name__ == '__main__':
    # input_img = os.path.join(get_img_dir(), 'star_transparent.png')
    image = Image.open('image3.png')
    width, height = image.size
    center = (int(0.5 * width), int(0.5 * height))
    black = (0, 0, 0, 255)
    ImageDraw.floodfill(image, xy=center, value=black)
    image.save('image5.png')

    print('Using Python version {}'.format(sys.version))
    print('Using Pillow version {}'.format(PILLOW_VERSION))