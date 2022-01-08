from flask import Flask, render_template, redirect
from werkzeug.utils import redirect
# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo
#Import web scraping code
from scrape_mars import *

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#set route
@app.route("/")
def home():
    
   
    mars_dict = mongo.db.mars_dict.find_one()
    # print(mars_dict)
    return render_template("index.html", mars=mars_dict)

    
@app.route("/scrape")
def scraper():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape()
    print(mars_data)
    # mars_dict.update({}, mars_data, upsert=True)
    mars_dict.update_one({}, {"$set": mars_data}, upsert=True)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)