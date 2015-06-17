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
query = query[:10]

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
		feature_array = img_from_url(url)
		artwork_features.append(feature_array)
		artists.append(art_dict[url])
		artwork_urls.append(url)

	# try: 
	# 	if key.endswith(".gif"):
	# 		pass
	# 		# urllib.urlretrieve(key, "image.gif")
	# 		# art = Artwork("image.gif") # loads art and channels

	# 	elif key.endswith("jpg"):
	# 	 	urllib.urlretrieve(key, "image.jpg")
	# 		art = Artwork("image.jpg") # loads art and channels

	# 	elif key.endswith("png"):
	# 	 	urllib.urlretrieve(key, "image.png")
	# 		art = Artwork("image.png") # loads art and channels

	# 	else: 
	# 		pass

	# 	
		

	# 	blue = art.blue()
	# 	green = art.green()
	# 	red = art.red()
	# 	gray = art.grayscale()

	# 	print "Now extracting features from artwork"
	# 	feature_array = [] # will fill with features
	# 	for channel in [blue, green, red, gray]:
	# 		art_char = [avg_intensity(channel), 
	# 		intensity(channel, "high"), 
	# 		intensity(channel, "medium"), 
	# 		intensity(channel, "low")]
	# 		feature_array.extend(art_char)
	 
		
		# print feature_array
	


	except:
		print "url no longer functioning :("

	num_art -= 1
	print "there are %i art pieces left" % num_art	
	# print ife.avg_intensity(art.blue())

# print artists
# print artwork_urls
# print artwork_features

# generate list of urls

# grab image and store temporarily





# # extracts features and adds to data frame
# col_names = ["avg_blue", "high_blue", "med_blue", "low_blue",
# 	"avg_green", "high_green", "med_green", "low_green",
# 	"avg_red", "high_red", "med_red", "low_red",
# 	"avg_gray", "high_gray", "med_gray", "low_gray"]

# index = [artists, artwork_urls]

df = pd.DataFrame(artwork_features)  
index = [artists,artwork_urls]
# df = pd.concat([artists, artwork_urls, df])
print "Done! Now writing to file!"
df.to_csv("artwork_features.csv")
# df.set_index(artwork_urls)

