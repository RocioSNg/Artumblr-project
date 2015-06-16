#-----------------------------------------------------------#
#			Tumblr Artist Blogname Miner								#
#			Author: Rocio Ng								#
#			Purpose: Extract artist blog names 				#
#			from the Tumblr API by scraping posts			#
#			tagged 'artist on tumblr' and adds				#
#			them to the tumblr_db database					#
#-----------------------------------------------------------#

from API_functions import find_artists
from secret import SQL_password
import pymysql as mdb

print "Making calls to the Tumblr API"
print "Starting to collect blog names from posts tagged 'artist on tumblr'"

# collecected up to 1433326512
# 3600s in a hour
# 86400s in a day
# 604800s in a week
# 2592000 in 30 days (month)

# Tumblr API only allows for 20 blognames to be returned at a time.
# allow for calls to api to find artist at multiple time stamps:
time_stamp = 1433426522
time_stamp = 1434058026 # use latest time stamp

time_stamp = time_stamp - (15 * 2592000) # start from 6 months ago
time_past = time_stamp - (12 * 2592000)
 # by month
increment = 3600  # hour


# establish connection to the SQL database
con = mdb.connect('localhost','root', SQL_password, 'tumblr_db')


while time_stamp > time_past:

	# collects a list of blog names,  tumblr API only lets you grab 20 at a time
	artist_list = find_artists(time_stamp)  

	num_artists = 0 # for collecting the unique artists actually found with each run

	with con:
		cur = con.cursor()
		for blog_name in artist_list:
			try:
				# Enter blog name into the database, Unique ID numbers are assigned
				cur.execute("INSERT INTO Artists(Blog_Name) VALUES(%s)", (blog_name))
				print "Now adding %s to the database" % blog_name
				num_artists += 1
			# Exception added so code doesn't break when duplicate is found
			except:
				print "Duplicate entry artist not added" 
	# Calls to the API can be made at different time points to get more than 20 artist blognames
	time_stamp -=  increment 

print "Artist Blogname miner completed. %i new unique artists added to the database" % num_artists
# for testing:
# with con:
#    cur = con.cursor()
#    cur.execute("SELECT * FROM Artists")
#    rows = cur.fetchall()
#    for row in rows:
#        print row

