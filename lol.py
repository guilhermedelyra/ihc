import os, numpy, PIL
from PIL import Image

# Access all PNG files in directory
allfiles=os.listdir(os.getcwd())
imlist=['image1.png', 'black3.png']

# Assuming all images are the same size, get dimensions of first image
w,h=Image.open(imlist[0]).size
N=len(imlist)

# Create a numpy array of floats to store the average (assume RGB images)
arr=numpy.zeros((h,w,3),numpy.float)

# Build up average pixel intensities, casting each image as an array of floats
for im in imlist:
	imarr = numpy.array(Image.open(im),dtype=numpy.float)
	imarr[:] = [[[z-z if z >= 220 else z for z in x] for x in l] for l in imarr]
	arr += imarr/N

# Round values in array and cast as 8-bit integer
arr=numpy.array(numpy.round(arr),dtype=numpy.uint8)

# Generate, save and preview final image
out=Image.fromarray(arr,mode="RGB")
out.save("Average.png")
out.show()