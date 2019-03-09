from flask import Flask, render_template, redirect
from flask_pymongo import pymongo 
import scrape_mars


#Create instance of Flask app
app = Flask(__name__)
#Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars 


# Create a root route / that will query your Mongo DB and pass the mars data into an HTML template to display the data.
@app.route("/")
def echo():
	mars = db.mars.find_one()
	#mars = mongo.db.mars.find_one()
	return render_template("index.html", mars=mars)


#Scrape the data
@app.route("/scrape")
def scrp():
	mars = db.mars
	#mars = mongo.db.mars
	data = scrape_mars.scrape()
	mars.update({}, data, upsert=True)
	return redirect("/") 




if __name__ == "__main__":
	app.run(debug=True)
