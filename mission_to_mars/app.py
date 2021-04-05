# Flask App
# importing dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# creating an instance of flask
app = Flask(__name__)


# creating a connection to MongoDB
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_database")

# Route to index page to render Mongo data to template
@app.route("/")
def index():

    # Find one record of data from Mongo
    mars_data = mongo.db.collection.find_one()
    
    # Activate jinja within the website index page
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():

    # Run the scrape function for Mars 
    mars_data = scrape_mars.scrape()

    # mars.append
    mongo.db.collection.update({}, mars_data, upsert = True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

