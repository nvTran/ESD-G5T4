from flask import *
import paypalrestsdk as paypal
from paypalrestsdk import *
from flask_sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/bidding'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)


# Currently using bidID retrieved from database.
# Need to change to bidID retrieved from other microservices later.



# class ListBid(db.Model):
#     __tablename__ = 'bidItem'
#     bidID = db.Column(db.String(10), primary_key=True)
#     productID = db.Column(db.String(100), nullable=False)
#     sellerID = db.Column(db.String(10), nullable=False)
#     bidDateTime = db.Column(db.String(20), nullable=False)
#     buyerID = db.Column(db.String(10), nullable=False)
#     bidAmt = db.Column(db.Float(), nullable=False)
#     bidStatus = db.Column(db.String(20), nullable=False)
#     meetup = db.Column(db.String(100), nullable=False)

 
#     def __init__(self, bidID, productID, sellerID, buyerID, bidDateTime, bidAmt, bidStatus, meetup):
#         self.bidID = bidID
#         self.productID = productID
#         self.sellerID = sellerID
#         self.bidDateTime = bidDateTime
#         self.buyerID = buyerID
#         self.bidAmt = bidAmt
#         self.bidStatus = bidStatus
#         self.meetup = meetup

#     def json(self):
#         return {"bidID": self.bidID, "productID": self.productID, "sellerID": self.sellerID, "bidDateTime": self.bidDateTime, "buyerID": self.buyerID, "bidAmt": self.bidAmt, "bidStatus": self.bidStatus, "meetup": self.bidStatus }




paypal.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "ASWAtFfl_iT5f6x7dTBwChLqyHE8OA-aqbKEUJ1uXlZC5bFSNEL1XcdwBJqQ9oV9grKW-7j1jod3X68I",
    "client_secret": "EFPgiR2Ku0gSyOgjc7hkkxfTAc2R4mPFWKUPy_RxFgxWR-h6ko6uZLjtFNgVd_ZLAHP8dHy6TkmGE92B"})



@app.route('/')
def index():
    #Can beautify this and link to Bid HTML Page. 
    return render_template("payment.html", **locals())


@app.route('/paypal_Return', methods=['GET'])
def paypal_Return():

    # ID of the payment. This ID is provided when creating payment.
    paymentId = request.args['paymentId']
    payer_id = request.args['PayerID']
    payment = paypal.Payment.find(paymentId)

    # PayerID is required to approve the payment.
    if payment.execute({"payer_id": payer_id}):  # return True or False
        print("Payment[%s] execute successfully" % (payment.id))
        # Can return back to a HTML Page. 
        return 'Payment execute successfully!' + " Your Payment ID is: " + payment.id
    else:
        print(payment.error)
        # Can return back to a HTML Page. 
        return 'Payment cannot be executed! ERROR occurs!'


@app.route('/paypal_payment', methods=['GET', 'POST'])
def paypal_payment():
    if request.method == 'POST':
        content = request.json
        productName = content['productName']
        bidID = content['bidID']
        bidAmt = content['bidAmt']
    
    # Payment
    # A Payment Resource; create one using
    # the above types and intent as 'sale'
    payment = paypal.Payment({
        "intent": "sale",

        # Payer
        # A resource representing a Payer that funds a payment
        # Payment Method as 'paypal'
        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5005/paypal_Return?success=true",
            "cancel_url": "http://127.0.0.1:5005/paypal_Return?cancel=true"},

        # Transaction
        # A transaction defines the contract of a
        # payment - what is the payment for and who
        # is fulfilling it.
        "transactions": [{

            # ItemList
            "item_list": {
                "items": [{
                    "name": productName,
                    "sku": bidID,
                    "price": str(bidAmt),
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": str(bidAmt * 1),
                "currency": "USD"},
            "description": "test 123 This is the payment transaction description."}]})

    # Create Payment and return status
    if payment.create():
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                # Convert to str to avoid google appengine unicode issue
                # https://github.com/paypal/rest-api-sdk-python/pull/58
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return jsonify({"redirect_url": redirect_url, "paymentID": payment.id })

    else:
        print("Error while creating payment:")
        print(payment.error)
        return "Error while creating payment"


if __name__ == '__main__':
    app.run(port=5005, debug=True)
