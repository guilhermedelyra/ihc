import glob
import re
import os

rgx = re.compile(r'[A-Za-z0-9]+_[A-Za-z0-9]+_g+\.jpg')
idx = re.compile(r'.*?_index+_g+\.jpg$')
for categories in glob.iglob('Jojogos/lib/etc/product_data/product-images/*/', recursive=True):
	for product in glob.iglob(categories+'/*/', recursive=True):
		imgs = list(glob.iglob(product+'/*.jpg'))

		imgs = [i.split('/')[-1] for i in imgs]

		contain_index = list(filter(idx.match, imgs))

		if (not contain_index):
			old_index = list(filter(rgx.match, imgs))[0]
			idx_slices = old_index.split('_')
			new_index = idx_slices[0]+'_index_'+idx_slices[2]
			os.rename(product+old_index, product+new_index)

		if (len(contain_index) > 1):
			old_index = list(filter(rgx.match, imgs))[0]
			idx_slices = old_index.split('_')
			new_index = idx_slices[0]+'_xxx_'+idx_slices[2]
			os.rename(product+old_index, product+new_index)
