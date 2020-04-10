from flask import Flask, request, jsonify
from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
import googlemaps
import requests



model = None
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

userID = 1
userName = "Name"
@app.route("/authenticate", methods =["POST"])
def authenticate():
    if request.method == "POST":
        global userID
        global userName
        content = request.json
        userID = content['id']
        userName = content['name']
        return "authenticated",201

# Home page that view links to all the functions and 
@app.route("/homepage", methods =["GET","POST"])
def homepage():
    if request.method == "GET":
        recent_products = requests.get("http://127.0.0.1:5001/recent_products")
        recent_products = recent_products.json()

        return render_template("homepage.html", userName=userName, userID = userID, recent_products = recent_products)
    if request.method == "POST":
        search_term = request.form['search_term']
        search_products = requests.post("http://127.0.0.1:5001/search_products", json={"search_term": search_term})
        search_products = search_products.json()
        if search_products['message'] == "product found":
            return render_template("search.html", search_products = search_products)


# View all products on the platform
@app.route("/recent_products/<string:userID>")
def all_products():
    all_products = request.get("http://127.0.0.1:5001/recent_products")
    response = all_products.json()
    return render_template("recent_products.html", all_products = response )







# View all products listed by a user
@app.route("/getProductByUserId/<string:userID>", methods=["GET"])
def getProductByUserId(userID):
    url = "http://127.0.0.1:5001/getProductByUserId/" + userID
    all_products = requests.get(url)
    all_products = all_products.json()
    if all_products['message'] == "successful":
        return render_template("products_by_user.html", all_products = all_products, userID = userID)




# View a product info
@app.route("/get_product_info/<string:productID>", methods=["GET"])
def get_product_info_by_productID(productID):
    url = "http://127.0.0.1:5001/get_product_info/" + productID
    product_info = requests.get(url)
    product_info = product_info.json()
    return render_template("product_info.html", product_info=product_info, userID=userID)
    



# post a new product
@app.route("/post_new_product", methods=["POST","GET"])
def post_new_product():
    if request.method == "GET":
        return render_template("posting.html", userID = userID)
    if request.method == "POST":
        productName = request.form['productName']
        productType = request.form['productType']
        productDesc = request.form['productDesc']
        meetup = request.form['meetup']

        post_new_product_request = requests.post('http://127.0.0.1:5001/post_new_product', json={"userID":userID, "productName": productName, "productType":productType, "productDesc": productDesc, "meetup":meetup})
        response = post_new_product_request.json()
        return render_template("blank1.html", message=  response['message'])


#View all offers for your products
@app.route("/view_offers/<string:productID>", methods=['POST',"GET"])
def seller_view_offers(productID):
    if request.method == "GET":
        url = 'http://127.0.0.1:5004/seller_view_bids/' + productID
        offers = requests.get(url)
        offers = offers.json()
        return render_template("view_offers.html", offers = offers)
    if request.method == "POST":
        # Update bid status
        bidID = request.form['bidID']
        url = "http://127.0.0.1:5004/change_bid_status/" + productID +"/"+ bidID
        register_selected_bid = requests.get(url)
        change_bid_status = register_selected_bid.json()
        # Update product status
        url2 = "http://127.0.0.1:5001/update_product_status"
        update_product = requests.post(url2, json={"productID": productID})
        update_product = update_product.json()
        return render_template("blank2.html", message1 = change_bid_status['message'], message2=update_product['message'])
        

#Place a bid for a product
@app.route("/place_bid/<string:sellerID>/<string:productID>", methods=['POST',"GET"])
def place_bids(sellerID,productID):
    if request.method == "GET":
        return render_template("place_bid.html")
    if request.method == 'POST':
        print(request.form)
        bidAmt = request.form['bidAmt']
        meetup = request.form['meetup']
        place_a_bid = requests.post('http://127.0.0.1:5004/place_bid/', json={"productID":productID, "buyerID": userID, "sellerID":sellerID, "bidAmt": bidAmt, "meetup":meetup})
        response = place_a_bid.json()
        return render_template("blank1.html", message = response['message'])

# View all bids placed by user
@app.route("/views_bid_and_status_by_userID", methods=["GET"])
def get_bids_and_status_by_buyerID():
    url = "http://127.0.0.1:5004/views_bid_and_status_by_userID/" + userID
    all_bids = requests.get(url)

    all_bids = all_bids.json()
    if all_bids['message'] == "successful":
        return render_template("bid_status.html", all_bids=all_bids)
    else:
        return render_template("bid_status.html", all_bids= "No bid found")
    
# transfer money to seller who accepted your bid.
@app.route("/transfer/<string:bidID>/<string:bidAmt>", methods=["GET","POST"])
def transfer(bidID,bidAmt):
    if request.method == "GET":
        return render_template("sure_to_transfer.html")

    if request.method == "POST":
        url = "http://127.0.0.1:5005/paypal_payment"
        transfer_request = requests.post(url, json={"bidID": bidID,"bidAmt": bidAmt,"productName": "ke me may"})
        transfer_request = transfer_request.json()
        return render_template("blank3.html", transfer_request=transfer_request)   



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
