# -*- coding: utf-8 -*-

import os
import braintree

from flask import Flask, redirect, url_for, json, request
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import date, datetime, timedelta

app = Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app.secret_key = os.environ.get('APP_SECRET_KEY')

braintree.Configuration.configure(
    os.environ.get('BT_ENVIRONMENT'),
    os.environ.get('BT_MERCHANT_ID'),
    os.environ.get('BT_PUBLIC_KEY'),
    os.environ.get('BT_PRIVATE_KEY')
)

@app.route("/")
def index():
    '''
    Index URI
    '''
    return redirect(url_for('new_token'))

@app.route('/token', methods=['GET'])
def new_token():
    '''
    Token access URI
    '''
    client_token = braintree.ClientToken.generate()
    response = app.response_class(
        response=json.dumps({
            "client_token": client_token
        }),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route("/load", methods=["POST"])
def load():
    '''
    Submission of load
    '''

    def search_for_transactions(customer, start, end):
        '''
        reusable code, refactoring out.
        '''
        return braintree.Transaction.search(
          braintree.TransactionSearch.customer_id == customer,
          braintree.TransactionSearch.created_at.between(start, end)
        )

    def create_rejection(msg):
        return app.response_class(
            response=json.dumps({
                "error": msg
            }),
            status=400,  # sematically using generic error
            mimetype='application/json'
        )

    nonce_from_the_client = request.form['payment_method_nonce'] # To come from payload and retrieved via /token request
    customer_id = request.form['customer_id']  # To come from payload
    amount_to_load = request.form['amount']  # To come from payload

    today = date.today()
    yesterday = today + timedelta(days=-1)  # not sure if this should be minus one minute as well.
    # Search for todays transactions
    todays_transactions = search_for_transactions(
        customer_id,
        datetime(today.year, today.month, today.day),
        datetime(yesterday.year, yesterday.month, yesterday.day)
    )
    todays_amount = sum([i['amount'] for i in todays_transactions.items if i['amount'] > 0])
    if(todays_amount < 500):  # Check less that £500
        # Search for the last 30 days transactions
        thirty_days_ago = today + timedelta(days=-30)   # not sure if this should be minus one minute as well.
        thirty_days_transactions = search_for_transactions(
            customer_id,
            datetime(today.year, today.month, today.day),
            datetime(
                thirty_days_ago.year,
                thirty_days_ago.month,
                thirty_days_ago.day
            )
        )
        thirty_days_amount = sum([i['amount'] for i in todays_transactions.items if i['amount'] > 0])
        if(thirty_days_amount < 800 ):  # Check less that £800
            # Search for the last 365 days transactions
            year_ago = today + timedelta(days=-365)  # not sure if this should be minus one minute as well.
            one_year_transactions = search_for_transactions(
                customer_id,
                datetime(today.year, today.month, today.day),
                datetime(year_ago.year, year_ago.month, year_ago.day)
            )
            one_year_amount = sum([i['amount'] for i in todays_transactions.items if i['amount'] > 0])
            if(one_year_amount < 2000 ):  # Check less that £2000
                # Get all transactions to determine balance
                # would probably never do this as is a large over head for each transaction but current single point of truth.
                all_transactions = braintree.Transaction.search(
                  braintree.TransactionSearch.customer_id == customer_id
                )
                balance = sum([i['amount'] for i in all_transactions.items])
                if(balance < 1000 ):  #  Check current balance is less than £1000
                    # load money
                    result = braintree.Transaction.sale({
                        "amount": amount_to_load,
                        "payment_method_nonce": nonce_from_the_client,
                        "options": {
                            "submit_for_settlement": True
                        }
                    })
                    if(result.is_success):
                        response = app.response_class(
                            response=json.dumps({
                                "transaction": result.transaction.id  # keeping it simple for now :)
                            }),
                            status=200,
                            mimetype='application/json'
                        )
                    else:
                        response = create_rejection("failed to transaction money because: %s" % result.message)
                #  More than £1000 reject
                else:
                    response = create_rejection(
                        "Your balance must be less £1000 to load more."  # provide good error response.
                    )
            #  More than £2000 reject
            else:
                response = create_rejection(
                    "You have loaded more that £800 in the last 365 days."  # provide good error response.
                )
        else:#  More than £800 reject
            response = create_rejection(
                "You have loaded more that £800 in the last 30 days."  # provide good error response.
            )
    else:  #  More than £500 reject
        response = create_rejection(
            "You have loaded more that £500 today."  # provide good error response.
        )
    return response

if __name__ == "__main__":
    app.run()
