from flask import render_template, request
from app import app
import pymysql as mdb
from secret import SQL_password
from art_matcher_algorithm import art_match
import urllib


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






@app.route('/output')
@app.route('/output/<url>')

def art_output(url=None):
    # if url == None:
    query_url = request.args.get('ID')
    # else:
    #     query_url = "http://37.media.tumblr.com/c4f9be2de49a997933cc3d5c78a36328/tumblr_n2cuiaAG3p1t7b5qro5_r1_1280.jpg"
    #     print query_url


    # check to make sure a real image is being uploaded
    true_image = False

    if query_url.endswith("jpg") or query_url.endswith("png"):
        true_image = True

    if true_image == False:
        return render_template("error.html")



    else:

        #add exception for when user does not put in an image
        try:
            url_list = art_match(query_url)
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

        except:
            return render_template("error.html")


    # for result in query_results:
    return render_template("output.html", origurl = query_url, artists=artists, artwork_url=artwork_url, artists_url=artists_url)   




    
    # for url in urls:
    
    # produces a lists of art urls that match the query
    

@app.route('/about')
def about():
    return render_template("about.html")

# @app.route('/slides')
# def slides():
#     return render_template("demo/demo.html")

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
