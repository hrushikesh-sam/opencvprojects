





import cv2 as cv
import numpy as np
import os


def detect_shapes(img):

	"""
	Purpose:
	---
	This function takes the image as an argument and returns a nested list
	containing details of colored (non-white) shapes in that image

	Input Arguments:
	---
	`img` :	[ numpy array ]
			numpy array of image returned by cv2 library

	Returns:
	---
	`detected_shapes` : [ list ]
			nested list containing details of colored (non-white)
			shapes present in image

	Example call:
	---
	shapes = detect_shapes(img)
	"""
	detected_shapes = []

	
	imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
	imgcan = cv.Canny(imgGray, 50, 50)

	conto, hier = cv.findContours(imgcan, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

	for cnt in conto:
		nest = []
		area = cv.contourArea(cnt)
		M = cv.moments(cnt)
		cx = int(M['m10'] / M['m00'])
		cy = int(M['m01'] / M['m00'])
		coordq = (cx, cy)

		px = img[cy, cx, 0]
		px1 = img[cy, cx, 1]
		px2 = img[cy, cx, 2]
		colormat = [px, px1, px2]
		if colormat == [255, 0, 0]:
			color = 'Blue'
		elif colormat == [0, 140, 255]:
			color = 'Orange'
		elif colormat == [0, 0, 255]:
			color = 'Red'
		elif colormat == [0, 255, 0]:
			color = 'Green'

		if area > 300:
			cv.drawContours(imgcan, cnt, -1, (255, 0, 0), 3)
			perim = cv.arcLength(cnt, True)

			approx = cv.approxPolyDP(cnt, 0.02 * perim, True)
			# print(len(approx))
			objcor = len(approx)
			x, y, w, h = cv.boundingRect(approx)

			if objcor == 3:
				objectType = "Triangle"
			elif objcor == 4:
				aspratio = w / float(h)
				if aspratio > 0.95 and aspratio < 1.05:
					objectType = "Square"
				else:
					objectType = "Rectangle"
			elif objcor == 5:
				objectType = "Pentagon"
			elif objcor == 6:
				objectType = "Hexagon"
			elif objcor > 6:
				objectType = "Circle"
		cx = str(cx)
		cy = str(cy)

		nest.append(color)
		nest.append(objectType)
		nest.append(coordq)
		detected_shapes.append(nest)
	
	 


	##################################################
	
	return detected_shapes

def get_labeled_image(img, detected_shapes):


	for detected in detected_shapes:
		colour = detected[0]
		shape = detected[1]
		coordinates = detected[2]
		cv.putText(img, str((colour, shape)),coordinates, cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
	return img

if __name__ == '__main__':
	
	# path directory of images in 'test_images' folder
	img_dir_path = 'test_images/'

	# path to 'test_image_1.png' image file
	file_num = 1
	img_file_path = img_dir_path + 'test_image_' + str(file_num) + '.png'
	
	# read image using opencv
	img = cv.imread(img_file_path)
	
	print('\n============================================')
	print('\nFor test_image_' + str(file_num) + '.png')
	
	# detect shape properties from image
	detected_shapes = detect_shapes(img)
	print(detected_shapes)
	
	# display image with labeled shapes
	img = get_labeled_image(img, detected_shapes)
	cv.imshow("labeled_image", img)
	cv.waitKey(2000)
	cv.destroyAllWindows()
	
	choice = input('\nDo you want to run your script on all test images ? => "y" or "n": ')
	
	if choice == 'y':

		for file_num in range(1, 16):
			
			# path to test image file
			img_file_path = img_dir_path + 'test_image_' + str(file_num) + '.png'
			
			# read image using opencv
			img = cv.imread(img_file_path)
	
			print('\n============================================')
			print('\nFor test_image_' + str(file_num) + '.png')
			
			# detect shape properties from image
			detected_shapes = detect_shapes(img)
			print(detected_shapes)
			
			# display image with labeled shapes
			img = get_labeled_image(img, detected_shapes)
			cv.imshow("labeled_image", img)
			cv.waitKey(2000)
			cv.destroyAllWindows()


