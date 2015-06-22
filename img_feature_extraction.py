#-----------------------------------------------------------#
#					Image feature extracter					#
#		Author: 	Rocio Ng								#
#		Purpose:	Functions and classes designed 			# 
#					to load images  						#
#					and extract features from image 	 	#
#					files using channels and edge 			#
#					detection, 	 							#
#-----------------------------------------------------------#

from __future__ import division
import numpy as np 
from numpy import array
import cv2
import urllib
import os

# class Artwork:
# 	def __init__(self, img_path):
# 		self.img_path = img_path
# 	'''extracts arrays of values of channels separately for image
# 	designated by image path and divides by 255 to convert
# 	to a fraction of intensity (value between 0 and 1)
# 	This also aids in normalization of the features. 
# 	'''
# 	# for RGB channels
# 	def blue(self):	
# 		return cv2.imread(self.img_path)[:,:,0]/255

# 	def green(self):
# 		return cv2.imread(self.img_path)[:,:,1]/255

# 	def red(self):
# 		return cv2.imread(self.img_path)[:,:,2]/255
# 	# for grayscale
# 	def grayscale(self):
# 		return cv2.imread(self.img_path, cv2.IMREAD_GRAYSCALE)/255

#-----------FEATURE EXTRACTION FROM DIFFERENT CHANNELS IN THE IMAGE-----------#

def BGR_channels(img_path):
	'''extracts arrays of values of BGR and G channels separately for the image
	divides by 255 to convert to a fraction of intensity (value between 0 and 1)
	This also controls for size of image
	'''
	img = cv2.imread(img_path)
	blue = img[:,:,0]/255
	green = img[:,:,1]/255
	red = img[:,:,2]/255
	gray = cv2.imread(img_path, cv2.COLOR_BGR2GRAY)
	gray = gray/255
	return blue, green, red, gray


def LAB_channels(img_path):
	'''extracts arrays of values of LAB channels separately for the image
	divides by 255 to convert to a fraction of intensity (value between 0 and 1)
	This also controls for size of image 
	'''
	img = cv2.imread(img_path, cv2.COLOR_BGR2LAB)
	l = img[:,:,0]/255
	a = img[:,:,1]/255
	b = img[:,:,2]/255
	return l,a,b

#----------functions on the extracted channels-----------------------#
def avg_intensity(channel):
	'''returns the average intensity of a 
	matrix for a channel
	'''
	return np.sum(channel)/np.prod(channel.shape)

def intensity(channel, grade):
	'''returns fraction of pixels that have	intensity higher 
	specified grade: low, medium, or high
	'''
	if grade == 'high':
		num_pixels = len(channel [np.where(channel >= .7)])
	if grade == 'medium':
		num_pixels = len(channel [np.where((channel < .7) & (channel > .3))])
	if grade == 'low':
		num_pixels = len(channel [np.where(channel <= .3)])

	return num_pixels/np.prod(channel.shape)
#---------------------------------------------------------------------------------------#




#------Extract features using edgedetecting and counting contours-----------------------#

class Converted_Image:
	def __init__(self, img_path):
		self.img_path = img_path
	'''Creates instance of image array and converts to a Contour
	drawing
	'''
	def convert(self):
		image = cv2.imread(self.img_path)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		blurred = cv2.GaussianBlur(gray, (3, 3), 0)
		edged = cv2.Canny(blurred, 30, 150)
		return edged

class Contour(Converted_Image):
	'''inherits from Converted_Image class'''
	def __init__(self, img_path):
		self.img_path = img_path
	def external(self):
		'''counts the external contours in the image'''
		edged = Converted_Image(self.img_path).convert()
		(_,external_cnts, _) = cv2.findContours(edged.copy(), 
			cv2.RETR_EXTERNAL, 
			cv2.CHAIN_APPROX_SIMPLE)
		return len(external_cnts)
	def total(self):
		''' counts the total contours in an image'''
		edged = Converted_Image(self.img_path).convert()
		(_,all_cnts, _) = cv2.findContours(edged.copy(), 
			cv2.RETR_LIST, 
			cv2.CHAIN_APPROX_SIMPLE)
		return len(all_cnts)


# # for testing
# art2 = Contour("C4.jpg")
# print art2.external()
# print art2.total()


#-------EXTRACTION OF FEATURES FROM SINGLE IMAGE--------------------#
def img_from_url(url):
	'''downloads simgle image from the url, extracts features 
	and returns them in an arry
	'''
	if url.endswith(".gif"): # we are not equipped for gifs yet..doh!
		pass
	elif url.endswith("jpg"):
		path = "image.jpg"
	elif url.endswith("png"):
		path = "image.png"
	else: 
		pass

	# download the image and saves it as the designated path
	# print "now downloading the image"
	urllib.urlretrieve(url, path)
	# extract channel info
	blue, green, red, gray = BGR_channels(path)
	l,a,b = LAB_channels(path)
	#extract contour info
	img_contour = Contour(path)
	tot_cont = img_contour.total()
	ext_cont = img_contour.external()
	int_cont = tot_cont - ext_cont # internal contors
	cont_ratio = ext_cont/int_cont
	# print cont_ratio

	# delete image file
	os.remove(path)

	feature_array = [] # will fill with features
	for channel in [blue, green, red, gray, l, a, b]:
		art_char = [avg_intensity(channel), 
		intensity(channel, "high"), 
		intensity(channel, "medium"), 
		intensity(channel, "low")]
		feature_array.extend(art_char)

	# add contour data to the feature array
	feature_array.extend([tot_cont, ext_cont, int_cont, cont_ratio])
	

	return feature_array


#for testing
#fv = img_from_url("http://www.cianellistudios.com/images/abstract-art/abstract-art-mother-earth.jpg")
#print fv

