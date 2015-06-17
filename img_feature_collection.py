import pymysql as mdb
from secret import SQL_password
from img_feature_extraction import *
import pandas as pd
import urllib


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
	cur.execute("SELECT Blog_Name, Img_url FROM Artwork")
	query = cur.fetchall()

# for testing
query = query[:200]

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
		feature_array = img_from_url(url) # extracts feature vector from image at url
		print len(feature_array)
		artwork_features.append(feature_array)
		artists.append(art_dict[url])
		artwork_urls.append(url)

	except:
		print "url no longer functioning :("

	num_art -= 1
	print "there are %i art pieces left" % num_art	

col_names = ["avg_blue", "high_blue", "med_blue", "low_blue",
	"avg_green", "high_green", "med_green", "low_green",
	"avg_red", "high_red", "med_red", "low_red",
	"avg_gray", "high_gray", "med_gray", "low_gray",
	"avg_l", "high_l", "med_l", "low_l",
	"avg_a", "high_a", "med_a", "low_a",
	"avg_b", "high_b", "med_b", "low_b",
	"tot_cont", "ext_cont", "int_cont", "con_ratio"]

index = [artists, artwork_urls]

df = pd.DataFrame(artwork_features, columns = col_names,
	index = [artists,artwork_urls])
# df = pd.concat([artists, artwork_urls, df])
print "Done! Now writing to file!"
df.to_csv("artwork_features.csv")
# df.set_index(artwork_urls)

