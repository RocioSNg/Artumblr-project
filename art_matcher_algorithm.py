#-----------------------------------------------------------#
#					Art Matcher 							#
#		Author: 	Rocio Ng								#
#		Purpose:	Implements K-means to cluster 			#
#					arwork based on feature vectors			#
#					and returns images closest to 			#
#					the query image in the feature 			#
#					space									#
#-----------------------------------------------------------#
from secret import SQL_password
import pymysql as mdb
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from img_feature_extraction import img_from_url
import scipy.spatial as sp
import pickle
from sklearn.externals import joblib
import time


# for testing:
# link = "http://www.cianellistudios.com/images/abstract-art/abstract-art-mother-earth.jpg"
# for future --- allow user to decide how many works to return

# def img_cluster():
# 	pass

#----------Convert SQL Image Feature Database to Pandas Dataframe-------------# 
def artwork_df():
	
	print "Now connecting to tumblr_db"
	con = mdb.connect('localhost',
		'root', 
		SQL_password, 
		'tumblr_db')

	with con:
		cur = con.cursor()
		print "Now extracting the feature space for all the images in the Database"
		# cur.execute("SELECT * FROM Artwork WHERE Avg_Gray is NOT NULL")
		sql = "SELECT * FROM Artwork WHERE Avg_Gray is NOT NULL"
		# query = cur.fetchall()
		art_df = pd.read_sql(sql, con)
		# get rid of unwanted columns
		art_df = art_df.drop(["Id", "Tags", "Notes"], axis =1)
		art_df = art_df.set_index(["Blog_Name", "Img_url"])
	
	return art_df
		#print art_df.head()

#-----Have csv pre-loaded to save processing time on the web-application-------#
# artwork_df = artwork_df()
# artwork_df.to_csv("art_df.csv")


def k_means():
	# load the feature space of art images in the database
	# art = pd.DataFrame.from_csv('data/artwork_features_MVP.csv', index_col= [0,1])

	art_df = artwork_df()


	#---------------Clustering on CHANNELS ONLY--------------------------#

	# include only channel columns
	art_df = art_df.loc[:,"Avg_Blue":"Low_Gray"]
	
	# drop avg gray column since it is mostly lumped along a single value
	art_df = art_df.drop("Avg_Gray", axis=1)


	# print channels_df.head()
	# run clustering algorithm and fit the model
	print "Now running the model"
	k_means = KMeans(n_clusters=9)
	k_means.fit(art_df)
	print "Now pickling the results of the model"
	clf = joblib.dump(k_means, "RGB_kmeans_model.pkl")


def art_match(url):
	'''downloads image at query url, extracts feature vector
	and returns the urls of art images in the database with vectors
	closest to the query image
	'''

	# load model results and database
	print "Now loading the Pickled K-means Fit"
	k_means = joblib.load('RGB_kmeans_model.pkl') 
	# art_df = artwork_df()
	print "Now loading art features dataframe"
	art_df = pd.DataFrame.from_csv("art_df.csv", index_col= [0,1])


	art_df = art_df.loc[:,"Avg_Blue":"Low_Gray"]
	art_df = art_df.drop("Avg_Gray", axis=1)
	
	print art_df.shape
	# load QUERY url and extracts the feature vector
	print "Loading the query image"
	query_img = img_from_url(url) # this has changed
	# include only channel features
	query_img = query_img[0:16] # last four have contour info
	print len(query_img)
	query_img.pop(12) # remove avg gray value
	
	print query_img

	# assign cluster number for query image
	print "Now assigning query image to a cluster"
	cluster = k_means.predict(query_img)[0]
	#cluster = predict[0] 

	print "Now extracting artwork from the same cluster"
	# extract the cluster that each art image belongs to
	labels = k_means.labels_
	# subset dataframe to only include images in the same
	# cluster as the query image
	indexes = np.where(labels == cluster)[0]
	art_subset = art_df.iloc[indexes]
	print "There are %i images in this cluster" % len(art_subset)

	#print art_subset.head()
	#cluster_center = k_means.cluster_centers_[cluster]

	start_time = time.time() # for checking time of matching

	print "Now finding matches to the query image"
	# calculate Eucldiean distances of art images to the query image
	nrows = int(art_subset.shape[0])
	distances = []

	for i in range(0,nrows):
	    row = list(art_subset.iloc[i]) 
	    distances.append(sp.distance.euclidean(row,query_img))

	print("--- %s seconds ---" % (time.time() - start_time))

	# adds noew column containing the distances    
	art_subset["Distance"] = distances

	

	# sort and extract the  6 closest images
	df = art_subset.sort('Distance').iloc[0:6]
	df.reset_index(inplace = True)
	# get urls they refer to
	artists = list(df["Blog_Name"])
	art_urls = list(df['Img_url'])

	return art_urls


# # # # for testing:
# link =  "http://www.cianellistudios.com/images/abstract-art/abstract-art-mother-earth.jpg"
# # # # for testing:
# art_match(link)



# if __name__ == '__main__':
# 	k_means()
# 	link =  "http://www.cianellistudios.com/images/abstract-art/abstract-art-mother-earth.jpg"
# # # # for testing:
# 	art_match(link)



def k_means_contour():
	pass
	# extract contour
	#art_df = artwork_df()
	print "Now loading art contour features"
	art_df = pd.DataFrame.from_csv("art_df.csv", index_col= [0,1])
	art_df = art_df.loc[:,"Avg_Blue":"Low_b"]