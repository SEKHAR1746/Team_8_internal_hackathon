from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

my_client = MongoClient("localhost", 27017)
my_db = my_client["mydatabase"]
my_collection = my_db["mycollection"]


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/paylater', methods=['GET', 'POST'])
def paylater():
    if request.method == 'POST':
        merchant = request.form.get('merchant')
        customer = request.form.get('customer')
        amount = float(request.form.get('amount'))

        transaction = {
            'merchant': merchant,
            'customer': customer,
            'amount': amount,
        }

        my_collection.insert_one({
            'merchant': merchant,'customer': customer,'amount':amount
        })

        return redirect('/paylater')

    return render_template('pay_later.html')

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    
    transactions = list(my_collection.find({}, {'_id': 0}))
    return render_template('transactions.html')


app.run(debug=True)