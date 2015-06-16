#-----------------------------------------------------------#
#			Tumblr Artist Blog General Info Miner 			#
#			Author: Rocio Ng								#
#			Purpose: Extracts general information 			#
#			about blogs (url, post count)					#
#			using blog names mined using the 				#
#			Artist Miner 									#
#-----------------------------------------------------------#

from API_functions import Tumblr_Artist
from secret import SQL_password
import pymysql as mdb

# Establish connection to the SQL database
print "Now connecting to tumblr_db"
con = mdb.connect('localhost','root', SQL_password, 'tumblr_db')

# Query the tumblr_db Artists table for blog names
with con:
	cur = con.cursor()
	# only select blog names that is missing information
	print "Now extracting blog names that are missing information"
	cur.execute("SELECT Blog_Name FROM Artists WHERE blog_url is null")
	blog_name_query = cur.fetchall()

# for testing
# blog_name_query = blog_name_query[1:10]

# convert query item into a list
blog_name_list = []
for blog_name in blog_name_query:
	blog_name_list.append(blog_name[0])

print blog_name_list

print "Making calls to the tumblr API"
for blog_name in blog_name_list:
	print "Adding info for blog name: %s" % blog_name
	
	artist = Tumblr_Artist(blog_name)
	name = artist.blog_name
	url = artist.blog_url()
	count = artist.posts_count()

	with con:
		cur = con.cursor()
		cur.execute("UPDATE Artists set blog_url=%s, posts_count=%s WHERE blog_name=%s", (url,count,name))
		cur.execute("SELECT * FROM Artists WHERE blog_name=%s", (name))

		rows = cur.fetchall()
		for row in rows:
			print row



# old code for wtriting to csv file

# print "Now adding information about blogs in the Database"
# # Need to allow for doing this for new artists on the database
# # wihtout looking them ALL up

# print "There are %i artists in total to be updated" % len(blog_name_list)

# for blog_name in blog_name_list:
# 	print "Adding info for user: %s" % blog_name

# 	# Create object instances for each artist
# 	artist = Tumblr_Artist(blog_name)

#  	# print artist.blog_name
#  	# print artist.blog_url()
#  	# print artist.posts_count()
#  	# artist_info = {artist.blog_name, 
#  	# [artist.blog_url(), artist.posts_count()]}

#  	all_artists[artist.blog_name] = [artist.blog_url(), 
#  	artist.posts_count()]









# # extract artist user names from text file
# with open('data/tumblr_artists_large.txt') as f:
# 	print "Now opening file containing list of artists"
# 	artist_list = list(csv.reader(f))[0]
# print "%i artist names in file" % len(artist_list)

# # get rid of duplicate artist:
# artist_list = list(set(artist_list))
# artist_list = filter(None, artist_list) # get rid of empty strings
# # print artist_list

# # index artist list if short on time:

# # artist_list = artist_list[0:500]


# all_artists = {}

# print "Now adding information about each blog"
# print "There are %i artists in total" % len(artist_list)

# for blog_name in artist_list:
# 	print "Adding info for user: %s" % blog_name
# 	artist = Tumblr_Artist(blog_name)
#  	# print artist.blog_name
#  	# print artist.blog_url()
#  	# print artist.posts_count()
#  	# artist_info = {artist.blog_name, 
#  	# [artist.blog_url(), artist.posts_count()]}
#  	all_artists[artist.blog_name] = [artist.blog_url(), 
#  	artist.posts_count()]

# print "Done! Now writing artists to file"

# # print all_artists
# df = pd.DataFrame.from_dict(all_artists, 'index')
# print df
# df.columns = ['url', 'posts_count']
# df.to_csv("artist_info.csv")
# # getting art from artist

# # import urllib
# # urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")