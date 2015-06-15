import pytumblr
from secret import *  # import needed authentification keys
import csv
# import json

# Authenticate Application 
client = pytumblr.TumblrRestClient(
	CLIENT_KEY,
	CLIENT_SECRET,
	TOKEN_KEY,
	TOKEN_SECRET
	)

# client.blog_info('rocio-ng.tumblr.com')
# followers = client.followers('rocio-ng.tumblr.com')
# print followers["total_users"]
# # test = json.dumps(followers.json())# returns json format

#----Get list of artist User names on Tumblr-------------#

def find_artists(time_stamp):
	'''get blognames from of blog posts that are tagged
	'artists on tumblr' at specified timestamp
	and returns list of blognames 
	'''
	artists = []

	# api call to get info about posts with tag
	# returns a list of dictionary objects
	artist_tagged = client.tagged("artists on tumblr", 
		before = time_stamp, limit = 20)
	
	# extract blog name (artist user name) and adds to list
	for post in artist_tagged:
		artists.append(str(post["blog_name"]))  # str gets rid of unicode

	artists =  list(set(artists)) # get rid of duplicates
	print "Adding %s unique artists" % len(artists)
	return artists

#----Get Info of a blog from an artist---------#
# 	seems more useful to use a Class ** see below **

# def get_blog_info(blog_name):
# 	blog_info = client.blog_info(blog_name)
# 	url = str(blog_info['blog']['url'])
# 	posts = str(blog_info['blog']['posts'])
# 	return {blog_name:[url, posts]}

#--------Get informaton regarding an Artist's blog-----------#

class Tumblr_Artist:
	'''Each instance of this class will refer to specific
	artist identified by blog_name
	'''
	def __init__(self, blog_name):
		self.blog_name = blog_name
	# def blog_info(self):
	# 	blog_info = client.blog_info(self.blog_name)
	# 	return blog_info
	def blog_url(self):
		'''gets blog url for the user'''
		blog_info = client.blog_info(self.blog_name)
		return str(blog_info['blog']['url'])
	def posts_count(self):
		'''gets number of posts by the user'''
		blog_info = client.blog_info(self.blog_name)
		return int(str(blog_info['blog']['posts']))

#-----Extract Artwork for each artist-----------#

def get_art(blog_name):
	art_posts = client.posts(blog_name, 
		type='photo', tag='art',
		limit = 20, reblog_info=False, notes_info=False)
	return art_posts

class Artwork:
	'''Each instance will refer to a specific piece of
	artwork for each artist in the artist list'''
	def __init__(self, blog_name):
		pass
# print get_art('rocio-ng.tumblr.com')