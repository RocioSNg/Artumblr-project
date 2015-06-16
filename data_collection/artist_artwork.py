#-----------------------------------------------------------#
#			Tumblr Artwork Miner				 			#
#			Author: Rocio Ng								#
#			Purpose: Extracts information and urls			#
#			for Original Artwork posted by 					#
#			artists obtained from Artist Miner 				#
#-----------------------------------------------------------#

from API_functions import get_art
from secret import SQL_password
import pymysql as mdb
import pandas as pd 
import json
import csv

# need to make sure art is NOT a REBLOG option is there


# Establish connection to the SQL database
print "Now connecting to tumblr_db"
con = mdb.connect('localhost','root', SQL_password, 'tumblr_db')

# Query the tumblr_db Artists table for blog names

with con:
	cur = con.cursor()
	# only select blog names that is missing information
	print "Now extracting blog names from tumblr_db"
	cur.execute("SELECT Blog_Name FROM Artists")
	blog_name_query = cur.fetchall()

# for testing
# blog_name_query = blog_name_query[1:5]

# convert query item into a list
blog_name_list = []
for blog_name in blog_name_query:
	blog_name_list.append(blog_name[0])


# # extract artist user names from text file
# with open('data/tumblr_artists_large.txt') as f:
# 	print "Now opening file containing list of artists"
# 	artist_list = list(csv.reader(f))[0]
# print "%i artist names in file" % len(artist_list)

# # get rid of duplicate artist:
# artist_list = list(set(artist_list))
# artist_list = filter(None, artist_list) # get rid of empty strings
# artist_list.remove("sandersteins")
# # print artist_list
print "There are %i artists in total" % len(blog_name_list)

# # index artist list if short on time:
# # artist_list = artist_list[0:3]


# artists_artwork = {}


for blog_name in blog_name_list:
	print "now adding art for %s" % blog_name
	# artist = "angrygirlcomics"

	# make call to the tumblr API to return info regarding art posts
	art_dump =  get_art(blog_name)
	art_dump = art_dump["posts"][0:20] # pulls out dictionary with info we want
	print "Found %i pieces from artist: %s" % (len(art_dump), blog_name)
	#print json.dumps(art_dump, indent = 1)

	for i in range(0,len(art_dump)):
		# print art_dump
		art_post = art_dump[i]
		


		
		# collect information we want from API call returns
		# post_id = art_post["id"] # id refers to BLOG ID NOT ART ID
		# encode method gets rid of unicode format
		
		url = art_post["photos"][0]['original_size']['url'].encode('ascii', 'ignore')
		tags = art_post["tags"]
		tags = str([tag.encode('ascii', 'ignore') for tag in tags])
		try:
			notes = art_post["note_count"]
		except KeyError:  # key for notes not created in posts without notes
			notes = 0
			print "No notes found"
		# artists_artwork[post_id] = [blog_name, url, tags, notes]
		# print artists_artwork

		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO Artwork(Blog_Name, Img_url, Tags, Notes) VALUES (%s,%s,%s,%s)",(blog_name,url,tags,notes)) 
			
# print artists_artwork
with con:
   cur = con.cursor()
   cur.execute("SELECT * FROM Artwork")
   rows = cur.fetchall()
   for row in rows:
       print row




# 		artists_artwork[art_post["id"]] = [blog_name, 
# 		str(art_post["date"]), tags, str(art_post["note_count"])]
# print artists_artwork
	
# df = pd.DataFrame.from_dict(artists_artwork, 'index')

# # df.columns = ['blog_name', 'date', 'tags', "notes"]
# print df
# df.to_csv("artwork.csv")










# js = json.loads(art["posts"])
# print js[0:10]
# df = pd.DataFrame.from_dict(art)

# dat = json.load(art)
# df = pd.DataFrame(dat)