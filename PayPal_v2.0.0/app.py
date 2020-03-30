from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import paypalrestsdk


app = Flask(__name__)
#Make sure to change the connection accordingly
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:8889/product'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
db = SQLAlchemy(app)
 
class Product(db.Model):
    __tablename__ = 'product'
 
    bidID = db.Column(db.String(13), primary_key=True)
    productID = db.Column(db.String(13), nullable=False)
    currency = db.Column(db.String(64), nullable=False)
    bidAmt = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer)
 
    def __init__(self, bidID, productID, currency, bidAmt, quantity):
        self.bidID = bidID
        self.productID = productID
        self.currency = currency
        self.bidAmt = bidAmt
        self.quantity = quantity
 
    def json(self):
        return {"bidID": self.bidID, "productID": self.productID, "bidAmt": self.bidAmt, "currency": self.currency, "quantity": self.quantity}


paypalrestsdk.configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "ASWAtFfl_iT5f6x7dTBwChLqyHE8OA-aqbKEUJ1uXlZC5bFSNEL1XcdwBJqQ9oV9grKW-7j1jod3X68I",
  "client_secret": "EFPgiR2Ku0gSyOgjc7hkkxfTAc2R4mPFWKUPy_RxFgxWR-h6ko6uZLjtFNgVd_ZLAHP8dHy6TkmGE92B" })

@app.route('/', methods=['POST','GET'])
def index(bidID):
    
    if request.method == "GET":
        return render_template('index.html')
    if request.method == "POST":
        return redirect(url_for('payment', bidID = bidID))


@app.route('/payment/<string:bidID>', methods=['POST', 'GET'])
def payment(bidID):

    bid = Product.query.filter_by(bidID=bidID).first()

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/payment/execute",
            "cancel_url": "http://localhost:3000/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": bid.productID,
                    "sku": bid.bidID,
                    "price": bid.bidAmt,
                    "currency": bid.currency,
                    "quantity": bid.quantity}]},
            "amount": {
                "total": bid.bidAmt,
                "currency": bid.currency},
            "description": "This is the payment transaction description."}]})

    if payment.create():
        print('Payment success!')
    else:
        print(payment.error)

    return jsonify({'paymentID' : payment.id})

@app.route('/execute', methods=['POST'])
def execute():
    success = False

    payment = paypalrestsdk.Payment.find(request.form['paymentID'])

    if payment.execute({'payer_id' : request.form['payerID']}):
        print('Execute success!')
        success = True
    else:
        print(payment.error)

    return jsonify({'success' : success})

if __name__ == '__main__':
    app.run(port=3000, debug=True)