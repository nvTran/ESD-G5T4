from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid


model = None
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bidding'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class ListBid(db.Model):
    __tablename__ = 'bidItem'
    bidID = db.Column(db.String(10), primary_key=True)
    productID = db.Column(db.String(100), primary_key=True)
    sellerID = db.Column(db.String(10), nullable=False)
    bidDateTime = db.Column(db.String(20), nullable=False)
    buyerID = db.Column(db.String(10), nullable=False)
    bidAmt = db.Column(db.Float(), nullable=False)
    bidStatus = db.Column(db.String(20), nullable=False)
    meetup = db.Column(db.String(100), nullable=False)

 
    def __init__(self, bidID, productID, sellerID, bidDateTime, buyerID, bidAmt, bidStatus, meetup):
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


@app.route("/seller_view_bids/<string:sellerID>")
def seller_view_bids(sellerID):
    # authenticate first
    all_bids = ListBid.query.filter_by(sellerID=sellerID).all()
    to_return = jsonify({"all_bids": [bid.json() for bid in all_bids]})
    return render_template("seller_view_bids.html", all_bids = to_return)

@app.route("/place_bid/<string:productID>", methods=['POST',"GET"])
def place_bids(productID):
    # authenticate first
    if request == 'POST':
        data = request.bid_amount

        me = ListBid(uuid.uuid4(), productID, sellerID, buyerID, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bidAmt, "Toa Payoh")
        db.session.add(me)
        db.session.commit()

        # a ăn nói cẩn thận mà
        # tự dưng đe dọa a!!??
        
        

        # place bid here
        # redirect to product page with status change
        return redirect(url_for('upload_image', filename=filename))

    if request == 'GET':
        # view the page to place bid 
        to_return = ListBid.query.filter_by(productID=productID).first()
        return render_template("place_bid.html", product_info = to_return)
         


    return render_template("place_bid.html")
 
if __name__ == '__main__':
    app.run(port=5000, debug=True)