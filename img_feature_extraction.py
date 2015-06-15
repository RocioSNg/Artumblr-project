# Functions for loading and extracting features from images

from __future__ import division
import numpy as np 
from numpy import array
import cv2
import urllib

class Artwork:
	def __init__(self, img_path):
		self.img_path = img_path
	'''extracts BGR channels separately for image
	designated by image path and calculates average
	intensity 
	'''
	def blue(self):	
		return cv2.imread(self.img_path)[:,:,0]/255

	def green(self):
		return cv2.imread(self.img_path)[:,:,1]/255

	def red(self):
		return cv2.imread(self.img_path)[:,:,2]/255

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


def img_from_url(url):
	'''downloads simgle image from the url, extracts features 
	returns the RGB channels as an array
	'''
	if url.endswith(".gif"):
		'''we are not equipped for gifs yet..doh!
		'''
		pass
		# urllib.urlretrieve(url, "image.gif")
		# art = Artwork("image.gif") # loads art and channels

	elif url.endswith("jpg"):
	 	urllib.urlretrieve(url, "image.jpg")
		art = Artwork("image.jpg") # loads art and channels

	elif url.endswith("png"):
	 	urllib.urlretrieve(url, "image.png")
		art = Artwork("image.png") # loads art and channels

	else: 
		pass

	# pull out the channels
	blue = art.blue()
	green = art.green()
	red = art.red()

	print "Now extracting features from artwork"

	feature_array = [] # will fill with features
	for channel in [blue, green, red]:
		art_char = [avg_intensity(channel), 
		intensity(channel, "high"), 
		intensity(channel, "medium"), 
		intensity(channel, "low")]
		feature_array.extend(art_char)
 
	return feature_array


# fv = img_from_url("https://41.media.tumblr.com/3b3fae7e380fbc25f802cc5994730586/tumblr_n1xxqg9O4p1sedjuto1_500.jpg")
# print fv