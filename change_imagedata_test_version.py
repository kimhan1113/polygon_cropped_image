# 성공함 poloygon image save
import labelme
import cv2
import glob
import numpy as np
import json
from PIL import Image, ImageDraw
import os

annotations = glob.glob('*.json')

for anno in annotations :

	shp = []
	label = labelme.label_file.LabelFile(anno)
	image_name = label.filename
	image_name = os.path.splitext(image_name)[0]
	shape = label.shapes

	for i in shape:

		shapes = i['points']
		for j in shapes:
			k = tuple(j)
			shp. append(k)

		# shapes = np.array(shapes)
		im = Image.open(image_name+'.bmp').convert("RGBA")
		# im = Image.open('Fov002_1.bmp').convert("RGBA")
		# convert to numpy (for convenience)
		imArray = np.asarray(im)
		# create mas
		maskIm = Image.new('L', (imArray.shape[1], imArray.shape[0]), 0)
		ImageDraw.Draw(maskIm).polygon(shp, outline=1, fill=1)
		mask = np.array(maskIm)

		# assemble new image (uint8: 0-255)
		newImArray = np.empty(imArray.shape, dtype='uint8')

		# colors (three first columns, RGB)
		newImArray[:, :, :3] = imArray[:, :, :3]

		# transparency (4th column)
		newImArray[:, :, 3] = mask * 255

		# back to Image from numpy
		newIm = Image.fromarray(newImArray, "RGBA")
		newIm.save('polygon_'+ image_name+'.png')



		# print(shape)


	# image_data = label.load_image_file(label.imagePath)



	# imageHeight,imageWidth = cv2.imread(label.imagePath).shape[:2]
	#
	# label.save(label.filename,
	# 		   label.shapes,
	# 		   label.imagePath,
	# 		   imageHeight,
	# 		   imageWidth,
	# 		   imageData=image_data)
	
	
	