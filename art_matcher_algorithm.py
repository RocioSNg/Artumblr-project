#-----------------------------------------------------------#
#					Art Matcher 							#
#		Author: 	Rocio Ng								#
#		Purpose:	Implements K-means to cluster 			#
#					arwork based on feature vectors			#
#					and returns images closest to 			#
#					the query image in the feature 			#
#					space									#
#-----------------------------------------------------------#

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from img_feature_extraction import img_from_url
import scipy.spatial as sp


# for testing:
# url = "http://40.media.tumblr.com/bae2ac17797e7eb78038834afa7754e9/tumblr_nhk0vpni6P1teo717o1_1280.jpg"

# for future --- allow user to decide how many works to return

# def img_cluster():
# 	pass

def art_match(url):
	'''downloads image at query url, extracts feature vector
	and returns the urls of art images in the database with vectors
	closest to the query image
	'''

	# load the feature space of art images in the database
	art = pd.DataFrame.from_csv('data/artwork_features.csv', index_col= [0,1])
	
	# run clustering algorithm and fit the model
	k_means = KMeans(n_clusters=4)
	k_means.fit(art)

	# load QUERY url and extracts the feature vector
	query_img = img_from_url(url)

	# assign cluster number for query image
	print "Now assigning query image to a cluster"
	cluster = k_means.predict(query_img)[0]
	#cluster = predict[0] # just a number

	print "Now extracting artwork from the same cluster"
	# extract the cluster that each art image belongs to
	labels = k_means.labels_
	# subset dataframe to only include images in the same
	# cluster as the query image
	indexes = np.where(labels == cluster)[0]
	art_subset = art.iloc[indexes]

	#cluster_center = k_means.cluster_centers_[cluster]

	
	print "Now finding matches to the query image"
	# calculate Eucldiean distances of art images to the query image
	nrows = int(art_subset.shape[0])
	distances = []
	for i in range(0,nrows):
	    row = list(art_subset.iloc[i]) 
	    distances.append(sp.distance.euclidean(row,query_img))
	# adds noew column containing the distances    
	art_subset["Distance"] = distances

	# sort and extract the  5 closest images
	df = art_subset.sort('Distance').iloc[0:5]
	df.reset_index(inplace = True)
	# get urls they refer to
	artists = list(df['X'])
	art_urls = list(df['X.1'])

	return art_urls


# for testing:
# predictor(url)