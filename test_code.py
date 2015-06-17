from __future__ import division
import cv2
image = "test_image.jpg"

rgb = cv2.imread(image)
HSV = cv2.imread(image, cv2.COLOR_BGR2HSV)
gray = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
LAB =  cv2.imread(image, cv2.COLOR_BGR2LAB)

print rgb[:,:,0]
print "BREAK"
print HSV
print "BREAK"
print LAB[:,:,0]
# print HSV[:,:,0]
print len(HSV)

print rgb.shape
print HSV.shape
print LAB.shape

