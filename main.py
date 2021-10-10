from logging import error
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
import random


app = Flask(__name__)
API_KEY = "SecretKey"

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

# All records fetched from DB
cafes = db.session.query(Cafe).all()

@app.route("/")
def home():
    return render_template("index.html",cafes=cafes)

# gets random coffee place
@app.route("/random")   
def random_cafe():
    random_cafe = random.choice(cafes)
    return jsonify(
        cafe={
            "can_take_calls":random_cafe.can_take_calls,
            "coffee_price":random_cafe.coffee_price,
            "has_sockets":random_cafe.has_sockets,
            "has_toilet":random_cafe.has_toilet,
            "has_wifi":random_cafe.has_wifi,
            "id":random_cafe.id,
            "img_url":random_cafe.img_url,
            "location":random_cafe.location,
            "map_url":random_cafe.map_url,
            "name":random_cafe.name,
            "seats":random_cafe.seats
        }
    )

# gets all the coffee place from DB
@app.route("/all")
def all_cafe():
    cafe_list = []

    for cafe in cafes:
        cafe_ =  {
            "can_take_calls":cafe.can_take_calls,
            "coffee_price":cafe.coffee_price,
            "has_sockets":cafe.has_sockets,
            "has_toilet":cafe.has_toilet,
            "has_wifi":cafe.has_wifi,
            "id":cafe.id,
            "img_url":cafe.img_url,
            "location":cafe.location,
            "map_url":cafe.map_url,
            "name":cafe.name,
            "seats":cafe.seats
        }
        cafe_list.append(cafe_)

    return jsonify(cafe = cafe_list)

# searches for a coffee place at mentioned location
@app.route("/search")
def search():
    loc = request.args.get("loc")  

    cafe_ = Cafe.query.filter_by(location=loc).first()

    try:
        return jsonify(
            cafe={
                "can_take_calls":cafe_.can_take_calls,
                "coffee_price":cafe_.coffee_price,
                "has_sockets":cafe_.has_sockets,
                "has_toilet":cafe_.has_toilet,
                "has_wifi":cafe_.has_wifi,
                "id":cafe_.id,
                "img_url":cafe_.img_url,
                "location":cafe_.location,
                "map_url":cafe_.map_url,
                "name":cafe_.name,
                "seats":cafe_.seats
            }
        )
    except AttributeError:
        return jsonify(
            error="Sorry, we don't have cafe at that location."
        ), 404

# update the record of a coffee place by searching for it using id
@app.route("/update-price/<id>")
def update_price(id):
    updated_price = request.args.get("new_price")
    api_key = request.args.get("api_key")

    if api_key == API_KEY:
        try:
            price_update = Cafe.query.get(int(id))
            price_update.coffee_price = updated_price
            db.session.commit()
            return jsonify(
                success="Succesfully updated the price"
            ), 200
        except AttributeError:
            return jsonify(
                error={
                    "Not found": "Sorry no coffee house exist with that id"
                }
            ), 404
    else:
        return jsonify(error="Invalid API Key")

@app.route("/report-closed/<id>")
def delete_record(id):
    api_key = request.args.get("api_key")
    if api_key == API_KEY:
        try:
            cafe_ = Cafe.query.get(int(id))
            db.session.delete(cafe_)
            db.session.commit()

            return jsonify(success = "Succesfully deleted the record")
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            return jsonify(
                error = {
                    "Not Found": "Sorry the id isn't valid."
                }
            )
    else:
        return jsonify(
            error = {
                "Not Found": "Sorry the api key isn't valid."
            }
        )

if __name__ == '__main__':
    app.run(debug=True)
