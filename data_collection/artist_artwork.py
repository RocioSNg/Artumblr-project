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


print "There are %i artists in total" % len(blog_name_list)

# # index artist list if short on time:
# # artist_list = artist_list[0:3]

errors = 0

for blog_name in blog_name_list:
	print "now adding art for %s" % blog_name

	try:
		# make call to the tumblr API to return info regarding art posts
		art_dump =  get_art(blog_name)
		art_dump = art_dump["posts"][0:20] # pulls out dictionary with info we want
		print "Found %i pieces from artist: %s" % (len(art_dump), blog_name)
		#print json.dumps(art_dump, indent = 1)

		# cycle through up to 20 art posts that were returned with API call
		for i in range(0,len(art_dump)):
			# print art_dump
			art_post = art_dump[i]
			
			#----check to see if post is a "reblog"-------#
			# collect labels in json file
			labels = []
			for label in art_post:
				labels.append(label.encode('ascii', 'ignore'))	# encode method gets rid of unicode format
			# reblogged from id post only shows up in reblogged posts"
			# will not add those posts to the database
			if "reblogged_from_id" in labels:
				print "reblog found and not added!"

			else:
				# collect information we want from API call returns
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
				try:
					with con:
						cur = con.cursor()
						cur.execute("INSERT INTO Artwork(Blog_Name, Img_url, Tags, Notes) VALUES (%s,%s,%s,%s)",(blog_name,url,tags,notes)) 
						cur.execute("SELECT * FROM Artwork WHERE blog_name=%s", (blog_name))
					# check to see what is being added to the database
					# rows = cur.fetchall()
					# for row in rows:
					# 	print row
				except:
					print "Duplicate artwork: Not Added." # if that artowrk is already in the data base.
	except:
		print "unknown error"  # a small number of runs throw errors
		errors += 1

print "Done mining artwork. There were %i errors" % errors
# # print artists_artwork
# with con:
#    cur = con.cursor()
#    cur.execute("SELECT * FROM Artwork")
#    rows = cur.fetchall()
#    for row in rows:
#        print row


