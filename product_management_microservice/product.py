from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy



model = None
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/listing'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

class Product(db.Model):
    __tablename__ = 'postItem'
 
    productID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(10), primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    productType = db.Column(db.String(20), nullable=False)
    productDesc = db.Column(db.String(500), nullable=True)
    meetup = db.Column(db.String(100), nullable=False)
 
    def __init__(self, productID, userID, productName, productType, productDesc, meetup):
        self.productID = productID
        self.userID = userID
        self.productName = productName
        self.productType = productType
        self.productDesc = productDesc
        self.meetup = meetup

    def json(self):
        return {"productID": self.productID, "sellerID": self.userID, "productName": self.productName, "productType": self.productType,"productDesc": self.productDesc, "meetup": self.meetup }


@app.route("/seller_view_bids/<string:sellerID>")
def seller_view_bids(sellerID):
    # authenticate first
    all_bids = ListBid.query.filter_by(sellerID=sellerID).first()
    return render_template(seller_view_bids.html, **all_bids)

 
if __name__ == '__main__':
    app.run(port=5000, debug=True)