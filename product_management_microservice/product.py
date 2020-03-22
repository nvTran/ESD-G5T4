from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy



model = None
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/ListBid'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Product(db.Model):
    __tablename__ = 'listing'
 
    productID = db.Column(db.String(100), primary_key=True)
    sellerID = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    dateListed = db.Column(db.Datetime, nullable=False)
    buyerID = db.Column(db.String(10), nullable=False)
    bid_amount = db.Column(db.String(100), nullable=False)
 
    def __init__(self, productID, sellerID, description, dateListed, buyerID, bid_amount):
        self.productID = productID
        self.sellerID = sellerID
        self.description = description
        self.dateListed = dateListed
        self.buyerID = buyerID
        self.bid_amount = bid_amount

    def json(self):
        return {"productID": self.productID, "sellerID": self.sellerID, "description": self.description, "dateListed": self.dateListed,"buyerID": self.buyerID, "bid_amount": self.bid_amount }


@app.route("/seller_view_bids/<string:sellerID>")
def seller_view_bids(sellerID):
    # authenticate first
    all_bids = ListBid.query.filter_by(sellerID=sellerID).first()
    return render_template(seller_view_bids.html, **all_bids)

 
if __name__ == '__main__':
    app.run(port=5000, debug=True)