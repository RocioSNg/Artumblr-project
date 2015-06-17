import pytumblr
from secret import * 
import pymysql as mdb
import pandas as pd 
import json
import csv

client = pytumblr.TumblrRestClient(
	CLIENT_KEY,
	CLIENT_SECRET,
	TOKEN_KEY,
	TOKEN_SECRET
	)


print "Now connecting to tumblr_db"
con = mdb.connect('localhost','root', SQL_password, 'tumblr_db')

blog_name = "strugglewithproductivity"

def get_art(blog_name):
	art_posts = client.posts(blog_name, 
		type='photo', tag='art',
		limit = 10, reblog_info=True, notes_info=False)
	return art_posts


# print json.dumps(get_art(blog_name)["photos"], indent=2)

art = get_art(blog_name)
art = art["posts"][0:20]

for i in range(0, len(art)):
	art_post = art[i]

	# collect keys to see if reblogged_from is there
	keys = []
	for key in art_post:
		keys.append(key.encode('ascii', 'ignore'))

	if "reblogged_from_id" in keys:
		print "reblog!"
# art_posts = art["posts"][0]

# for key in art_posts:
# 	print key
