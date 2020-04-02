from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import googlemaps
from datetime import datetime
import uuid


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
    productStatus = db.Column(db.String(20), nullable=False)
    meetup = db.Column(db.String(100), nullable=False)
 
    def __init__(self, productID, userID, productName, productType, productDesc, productStatus, meetup):
        self.productID = productID
        self.userID = userID
        self.productName = productName
        self.productType = productType
        self.productDesc = productDesc
        self.productStatus = productStatus
        self.meetup = meetup

    def json(self):
        return {"productID": self.productID, "sellerID": self.userID, "productName": self.productName, "productType": self.productType,"productDesc": self.productDesc, "productStatus": self.productStatus, "meetup": self.meetup }


@app.route("/")
def welcome():
    return "Hello there, this is product microservice"

@app.route("/recent_products")
def recent_products():
    all_products = Product.query.limit(20).all()
    return jsonify({"all_products": [product.json() for product in all_products]}) 

# @app.route("/all_product/<string:userID>")
# def all_products(userID):
#     return render_template("all_products.html", userID = userID)

@app.route("/getProductByUserId/<string:userID>", methods=["GET"])
def getProductByUserId(userID):
    # authenticate first
    all_products = Product.query.filter_by(userID=userID).all()
    return jsonify({"message": "successful", "all_products": [product.json() for product in all_products]})

@app.route("/update_product_status", methods=["GET","POST"])
def update_product_status():
    # change product status to pending
    # change successful bid status from pending to accepted, pending paynent, create new entry for transaction db
    # once transaction completed, change bid to successful and product status to closed
    if request.method == 'POST':
        content = request.json
        productID = content['productID']

    product_queried = Product.query.filter_by(productID =productID).first()
    product_queried.productStatus = 'closed'
    db.session.commit()

    
    return jsonify({"message": "updated"})

@app.route("/get_product_info/<string:productID>", methods=["GET"])
def get_product_info_by_productID(productID):
    if request.method == 'GET':        
        product = Product.query.filter_by(productID=productID).first()
        if product:
            return jsonify({"message": [product.json() ]})
        return jsonify({"message": "product not found" })




@app.route("/post_new_product", methods=["POST","GET"])
def post_new_product():
    if request.method == 'POST':
        content = request.json
        productName = content['productName']
        productType = content['productType']
        productDesc = content['productDesc']
        sellerID = content["userID"]
        meetup = content['meetup']

        add_product = Product(str(uuid.uuid4())[:10], sellerID, productName, productType, productDesc, "newly listed", meetup)
        db.session.add(add_product)
        db.session.commit()
        # redirect to product page with status change
        return jsonify({"message": "successfully added a new product"})
    if request.method == 'GET':
        return "This is a page to post new product"

if __name__ == '__main__':
    app.run(port=5001, debug=True)