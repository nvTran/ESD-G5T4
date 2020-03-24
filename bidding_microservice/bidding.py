from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime


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


@app.route("/seller_view_bids/<string:sellerID>", methods=['POST',"GET"])
def seller_view_bids(productID):
    # authenticate first
    all_bids = ListBid.query.filter_by(productID=productID).all()
    to_return = jsonify({"all_bids": [bid.json() for bid in all_bids]})
    return render_template("seller_view_bids.html", all_bids = to_return)

@app.route("/place_bid/<string:productID>", methods=['POST',"GET"])
def place_bids(productID):
    # authenticate first to get buyerID

    if request.method == 'POST':
        bidAmt = request.form['bidAmt']
        meetup = request.form['meetup']

        add_bid = ListBid(str(uuid.uuid4())[:10], productID, "123", "357", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bidAmt, "pending", meetup)
        db.session.add(add_bid)
        db.session.commit()
        # redirect to product page with status change
        return "bid_placed"

    if request.method == 'GET':
        # view the page to place bid 
        to_return = ListBid.query.filter_by(productID=productID).first()
        return render_template("place_bid.html", product_info = to_return)
         


    return render_template("place_bid.html")
 
@app.route("/place_bid/<string:productID>", methods=["GET"])
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




# @app.route("/check_if_bid_exist_for_a_product/<string:productID>", methods=['GET'])
# def check_if_bid_exist_for_a_product(productID):
#     # get userID from authentication



if __name__ == '__main__':
    app.run(port=5000, debug=True)