from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',})
db = SQLAlchemy(metadata=metadata)


class Bank(db.Model, SerializerMixin):
    __tablename__ = 'banks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    accounts = db.relationship('Account', back_populates='bank')
    customers = association_proxy('accounts','customer')
    serialize_rules = ('accounts.bank')

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    accounts = db.relationship('Account', back_populates='customer')
    banks = association_proxy('accounts','bank')
    serialize_rules = ('-accounts.customer')


class Account(db.Model, SerializerMixin):
    __tablename__ = 'accounts'
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False, default=0)
    account_type = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    bank_id = db.Column(db.Integer, db.ForeignKey('banks.id'), nullable=False)
    bank = db.relationship('Bank', back_populates='accounts')
    customer = db.relationship('Customer', back_populates='accounts')


    @validates('balance')
    def negative_balance(self, key, value):
        if value<=0:
            raise ValueError('DON\'T BE BROKE')
        return value
    
    serialize_rules = ('-bank.accounts', '-customer.accounts')