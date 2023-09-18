#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Customer, Bank, Account

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

@app.get('/customers')
def get_customers():
    customers = Customer.query.all()
    return [customer.to_dict(rules=('-accounts',)) for customer in customers]

@app.get('/customers/<int:id>')
def get_customer_by_id(id):
    try:
        customer = Customer.query.filter(Customer.id == id).first()
        return customer.to_dict(), 200
    except:
        return{'error':'Customer doesn\'t exist'}, 404

@app.delete('/customer/<int:id>')
def delete_customer(id):
    try:
        customer = Customer.query.filter(Customer.id ==id).first()
        for account in customer.accounts:
            db.session.delete(account)
        db.session.delete(customer)
        db.session.commit()
    except:
        return{'error':'Customer not found'}, 404


@app.post('/accounts')
def create_account():
    try:
        data = request.json

        customer = Customer.query.filter(Customer.id == data['customer_id']).first()
        bank = Bank.query.filter(Bank.id == data['bank_id']).first()

        new_account = Account(
            account_type=data['account_type'],
            balance=data['balance'],
            customer=customer,
            bank=bank
            )
        
        db.session.add(new_account)
        db.session.commit()

        return new_account.to_dict(), 201
    except:
        return {'error': 'Something went wrong'}, 406
       

if __name__ == '__main__':
    app.run(port=5555, debug=True)