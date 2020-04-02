from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
import googlemaps


model = None
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bidding'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class ListBid(db.Model):
    __tablename__ = 'bidItem'
    bidID = db.Column(db.String(10), primary_key=True)
    productID = db.Column(db.String(100), nullable=False)
    sellerID = db.Column(db.String(10), nullable=False)
    bidDateTime = db.Column(db.String(20), nullable=False)
    buyerID = db.Column(db.String(10), nullable=False)
    bidAmt = db.Column(db.Float(), nullable=False)
    bidStatus = db.Column(db.String(20), nullable=False)
    meetup = db.Column(db.String(100), nullable=False)

 
    def __init__(self, bidID, productID, sellerID, buyerID, bidDateTime, bidAmt, bidStatus, meetup):
        self.bidID = bidID
        self.productID = productID
        self.sellerID = sellerID
        self.bidDateTime = bidDateTime
        self.buyerID = buyerID
        self.bidAmt = bidAmt
        self.bidStatus = bidStatus
        self.meetup = meetup

    def json(self):
        return {"bidID": self.bidID, "productID": self.productID, "sellerID": self.sellerID, "bidDateTime": self.bidDateTime, "buyerID": self.buyerID, "bidAmt": self.bidAmt, "bidStatus": self.bidStatus, "meetup": self.bidStatus }

@app.route("/")
def say_hello():
    return "This is bidding microservice"


@app.route("/seller_view_bids/<string:productID>", methods=['POST',"GET"])
def seller_view_offers(productID):
    # authenticate first
    if request.method == "GET":
        all_bids = ListBid.query.filter_by(productID=productID).all()
        return jsonify({"all_bids": [bid.json() for bid in all_bids]})
    


@app.route("/place_bid/", methods=['POST',"GET"])
def place_bids():
    # authenticate first to get buyerID

    if request.method == 'POST':
        print(request.form)
        bidAmt = request.form['bidAmt']
        meetup = request.form['meetup']

        gmaps = googlemaps.Client(key='AIzaSyDgHcefqn02VGMnzpAX3jBXoAoWvuLF3c0')
        # longitude = request.form['longitude']
        # latitude = request.form['latitude']
        # coords = str(latitude) + "," + str(longitude)``
        # reverse_geocode_result = gmaps.reverse_geocode((float(latitude), float(longitude)))

        add_bid = ListBid(str(uuid.uuid4())[:10], productID, "123", "357", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bidAmt, "pending", str(meetup))
        db.session.add(add_bid)
        db.session.commit()
        # redirect to product page with status change
        return jsonify({"message":"successful"}),200

    if request.method == 'GET':
        # view the page to place bid 
        to_return = ListBid.query.filter_by(productID=productID).first()
        return render_template("place_bid.html", product_info = to_return)
         


    return render_template("place_bid.html")
 
@app.route("/chang_bid_status/<string:productID>/<string:bidID>", methods=["GET"])
def change_bid_status_for_successful_bids(productID,bidID):
    all_bids = ListBid.query.filter_by(productID=productID).all()
    if all_bids: 
        for bid in all_bids:
            if bid.bidID == bidID:
                bid.bidStatus = 'successful'
                db.session.commit()
            bid.bidStatus = 'failed'
            db.session.commit()
        return jsonify({"message": "successfully updated bid status for all bids"}), 200
    return jsonify({"message": "couldnot find any bids for the productID specified"}), 200


@app.route("/views_bid_and_status_by_userID/<string:buyerID>", methods=["GET"])
def get_bids_and_status_by_buyerID(buyerID):
    if request.method == "GET":
        all_bids = ListBid.query.filter_by(buyerID=buyerID).first()
        if all_bids:
            return jsonify({"message": "successful", "all_bids": [bid.json() for bid in all_bids]})
        else:
            return jsonify({"message": "couldnot find any bids made by userID specified"})


if __name__ == '__main__':
    app.run(port=5004, debug=True)