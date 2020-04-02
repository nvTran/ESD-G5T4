from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
import googlemaps
import requests



model = None
app = Flask(__name__)
CORS(app)

userID = "christine" 

# Home page that view links to all the functions and 
@app.route("/homepage")
def homepage():
    recent_products = requests.get("http://127.0.0.1:5001/recent_products")
    recent_products = recent_products.json()

    return render_template("homepage.html", userID = userID, recent_products = recent_products)


# View all products on the platform
@app.route("/recent_products/<string:userID>")
def all_products():
    all_products = request.get("http://127.0.0.1:5001/recent_products")
    response = all_products.json()
    return render_template("recent_products.html", all_products = response )

# View all products listed by a user
@app.route("/getProductByUserId/<string:userID>", methods=["GET"])
def getProductByUserId(userID):
    url = "http://127.0.0.1:5001/getProductByUserId" + userID
    all_products = request.get("url")
    all_products = all_products.json()
    if all_products['message'] == "successful":
        return render_template("products_by_user.html", all_products = all_products['products'])




# View a product info
@app.route("/get_product_info/<string:productID>", methods=["GET"])
def get_product_info_by_productID(productID):
    url = "http://127.0.0.1:5001/get_product_info/" + productID
    product_info = requests.get(str(url))

    response = product_info.json()
    print(response)
    # {"productID": self.productID, "sellerID": self.userID, "productName": self.productName, "productType": self.productType,"productDesc": self.productDesc, "productStatus": self.productStatus, "meetup": self.meetup }
    return render_template("view_product.html", product_info=response)
    



# post a new product
@app.route("/post_new_product", methods=["POST","GET"])
def post_new_product():
    if request.method == "GET":
        return render_template("posting.html")
    if request.method == "POST":
        productName = request.form['productName']
        productType = request.form['productType']
        productDesc = request.form['productDesc']
        meetup = request.form['meetup']

        post_new_product_request = requests.post('http://127.0.0.1:5001/post_new_product', json={"userID":userID, "productName": productName, "productType":productType, "productDesc": productDesc, "meetup":meetup})
        response = post_new_product_request.json()
        return response['message']


#View all offers for your products
@app.route("/view_offers/<string:sellerID>", methods=['POST',"GET"])
def seller_view_bids(productID):
    offers = requests.get('http://127.0.0.1:5004/seller_view_bids/')
#     all_bids = ListBid.query.filter_by(productID=productID).all()
#     to_return = jsonify({"all_bids": [bid.json() for bid in all_bids]})
#     return render_template("seller_view_bids.html", all_bids = to_return)


#Place a bid for a product
@app.route("/place_bid/<string:productID>", methods=['POST',"GET"])
def place_bids(productID):
    if request.method == "GET":
        return render_template("place_bid.html")
    if request.method == 'POST':
        print(request.form)
        bidAmt = request.form['bidAmt']
        meetup = request.form['meetup']
        place_a_bid = requests.post('http://127.0.0.1:5001/post_new_product', json={"userID":userID, "productName": productName, "productType":productType, "productDesc": productDesc, "meetup":meetup})
        response = post_new_product_request.json()
        if response['message'] == "successful":
            return "successfully placed a bid"

# View all bids placed by user
@app.route("/views_bid_and_status_by_userID", methods=["GET"])
def get_bids_and_status_by_buyerID():
    url = "http://127.0.0.1:5001/views_bid_and_status_by_userID/" + userID
    all_bids = requests.get(str(url))

    response = all_bids.json()
    print(response)
    # {"productID": self.productID, "sellerID": self.userID, "productName": self.productName, "productType": self.productType,"productDesc": self.productDesc, "productStatus": self.productStatus, "meetup": self.meetup }
    return render_template("bid_status.html", all_bids=response)
    

if __name__ == '__main__':
    app.run(port=5002, debug=True)