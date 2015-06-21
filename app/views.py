from flask import render_template, request
from app import app
import pymysql as mdb
from secret import SQL_password
from art_matcher_algorithm import art_match


db = mdb.connect(user="root", host="localhost", 
	passwd=SQL_password, db="tumblr_db")

#----app.route() directs to different pages----#

# for the home page
@app.route('/')
@app.route('/index')
# loads code for the index "HOME" Page
# for now it is also serves as the "input" page
def index():
    return render_template("index.html")


# @app.route('/db')
# def cities_page():
#     with db:
#         cur = db.cursor()
#         cur.execute("SELECT Name FROM City LIMIT 15;")
#         query_results = cur.fetchall()
#     cities = ""
#     for result in query_results:
#         cities += result[0]
#         cities += "<br>"
#     return cities

# @app.route("/db_fancy")
# def cities_page_fancy():
#     with db:
#         cur = db.cursor()
#         cur.execute("SELECT Name, CountryCode, Population FROM City ORDER BY Population LIMIT 15;")

#         query_results = cur.fetchall()
#     cities = []
#     for result in query_results:
#         cities.append(dict(name=result[0], country=result[1], population=result[2]))
#     return render_template('cities.html', cities=cities)

# @app.route('/input')
# def cities_input():
#     return render_template("input.html")

@app.route('/output')

def art_output():
    query_url = request.args.get('ID')
    url_list = art_match(query_url)
    # for url in urls:
    
    # produces a lists of art urls that match the query
    img_matches = {}

    with db:
    	cur = db.cursor()
    	
        # for each art url find the artist name and blog url that matches
        print "now retrieving blog names for the matched art"
        for url in url_list:
            name = cur.execute("SELECT Artists.blog_name, Artists.blog_url FROM Artists,Artwork WHERE Artwork.img_url=%s AND Artists.blog_name = Artwork.blog_name",(url))
            query_results = cur.fetchall()
            # appends each in a diction
            # blog_info = []
            # for result in query_results:
            blog_info = [query_results[0][0], query_results[0][1]]    
            img_matches[url] = blog_info
    
    artwork_url=[]
    artists=[]
    artists_url = []
    for img in img_matches:
        artwork_url.append(img)
        artists.append(img_matches[img][0])
        artists_url.append(img_matches[img][1])

    # for result in query_results:
    return render_template("output.html", origurl = query_url, artists=artists, artwork_url=artwork_url, artists_url=artists_url)   
      

   
    # return render_template("output.html", origurl = query_url, 
    # 	urls = url_list, img_matches = img_matches, the_result = the_result)   


#url_list = []
# for url in urls:
#     url_list.append()

# def cities_output():

#     #pull 'ID' from input field and store it
#     city = request.args.get('ID')


#     with db:
#         cur = db.cursor()
#         #just select the city from the world_innodb that the user inputs
#         cur.execute("SELECT Name, CountryCode,  Population FROM City WHERE Name='%s';" % city)
#         query_results = cur.fetchall()

#     cities = []
#     for result in query_results:
#         cities.append(dict(name=result[0], country=result[1], population=result[2]))
#     the_result = ''
#     return render_template("output.html", cities = cities, the_result = the_result)
