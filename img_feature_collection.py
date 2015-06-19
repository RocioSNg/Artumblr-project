import pymysql as mdb
from secret import SQL_password
from img_feature_extraction import *
import pandas as pd
import urllib
# from numpy import tolist

con = mdb.connect('localhost', 
	'root', 
	SQL_password,
	'tumblr_db'
	)

print "Now connecting to tumblr_db"
con = mdb.connect('localhost','root', SQL_password, 'tumblr_db')
# Query the tumblr_db artwork table for blog names and artwork urls
with con:
	cur = con.cursor()
	# only select blog names that is missing information
	print "Now extracting blog names and artwork urls from tumblr_db"
	cur.execute("SELECT Blog_Name, Img_url FROM Artwork WHERE Avg_Blue is null")
	query = cur.fetchall()

# for testing
# query = query[]

num_art = len(query)
print " There are %i pieces to analyze" % num_art

art_dict = {} # keys are URLS and values are blog names
for row in query:
	art_dict[row[1]] = row[0]  

artists = [] # collect artist names (strings)
artwork_urls = [] # collect urls (strings)
artwork_features = [] # collect arrays of features (lists) 


for url in art_dict:  # for each ART url in the dictionary
	
	print "now downloading art from url: %s" % url
	try: 
		feature_np_array = img_from_url(url) # extracts feature vector from image at url
		print len(feature_np_array)
		# artwork_features.append(feature_array)
		# artists.append(art_dict[url])
		# artwork_urls.append(url)

		
	
	except:
		print "url no longer functioning :("
		continue

	# convert to python data type that can be read into SQL query
	print "getting features of image"
	feature_array = []
	for feature in feature_np_array:
		feature_array.append(str(feature))


	# for SQL inserts:
	with con:
		cur = con.cursor()
	
		# only select blog names that is missing information
		print "Now adding updating SQL Artwork data table"
		cur.execute("UPDATE Artwork SET Avg_Blue=%s WHERE Img_url=%s" , (feature_array[0], url))
		cur.execute("UPDATE Artwork SET Avg_Blue=%s, High_Blue=%s, Med_Blue=%s, Low_Blue=%s WHERE Img_url=%s" , (feature_array[0], feature_array[1], feature_array[2], feature_array[3], url))
		cur.execute("UPDATE Artwork SET Avg_Green=%s, High_Green=%s, Med_Green=%s, Low_Green=%s WHERE Img_url=%s", (feature_array[4], feature_array[5], feature_array[6],feature_array[7], url))
		cur.execute("UPDATE Artwork SET Avg_Red=%s, High_Red=%s, Med_Red=%s, Low_Red=%s WHERE Img_url=%s", (feature_array[8], feature_array[9], feature_array[10], feature_array[11], url))
		cur.execute("UPDATE Artwork SET Avg_Gray=%s, High_Gray=%s, Med_Gray=%s, Low_Gray=%s WHERE Img_url=%s", (feature_array[12], feature_array[13], feature_array[14], feature_array[15], url))
		cur.execute("UPDATE Artwork SET Avg_l=%s, High_l=%s, Med_l=%s, Low_l=%s WHERE Img_url=%s", (feature_array[16], feature_array[17], feature_array[18], feature_array[19], url))
		cur.execute("UPDATE Artwork SET Avg_a=%s, High_a=%s, Med_a=%s, Low_a=%s WHERE Img_url=%s", (feature_array[20], feature_array[21], feature_array[22], feature_array[23], url))
		cur.execute("UPDATE Artwork SET Avg_b=%s, High_b=%s, Med_b=%s, Low_b=%s WHERE Img_url=%s", (feature_array[24], feature_array[25], feature_array[26], feature_array[27], url))
		cur.execute("UPDATE Artwork SET Tot_Cont=%s, Ext_Cont=%s, Int_Cont=%s, Con_Ratio=%s WHERE Img_url=%s", (feature_array[28], feature_array[29], feature_array[30], feature_array[31], url))
		# query = cur.fetchall()

	# tracker
	num_art -= 1
	print "there are %i art pieces left" % num_art	





# col_names = ["avg_blue", "high_blue", "med_blue", "low_blue",
# 	"avg_green", "high_green", "med_green", "low_green",
# 	"avg_red", "high_red", "med_red", "low_red",
# 	"avg_gray", "high_gray", "med_gray", "low_gray",
# 	"avg_l", "high_l", "med_l", "low_l",
# 	"avg_a", "high_a", "med_a", "low_a",
# 	"avg_b", "high_b", "med_b", "low_b",
# 	"tot_cont", "ext_cont", "int_cont", "con_ratio"]

# index = [artists, artwork_urls]

# df = pd.DataFrame(artwork_features, columns = col_names,
# 	index = [artists,artwork_urls])
# # df = pd.concat([artists, artwork_urls, df])
# print "Done! Now writing to file!"
# df.to_csv("artwork_features.csv")
# # df.set_index(artwork_urls)

