import scipy.misc
import numpy as np

filename = 'image3.png'

img = (scipy.misc.imread(filename)).astype(float)
noise_mask = np.random.poisson(img)
noisy = np.random.poisson(img / 255.0 * 15) / 15 * 255  # noisy image
# noisemap = create_noisemap() 
# noisy = image + np.random.poisson(noisemap)
noisy_img = img + np.random.poisson(noisy)
scipy.misc.imsave('image6.png', noisy_img)