# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id              = db.Column(db.Integer,     primary_key=True)
    user            = db.Column(db.String(64),  unique = True)
    email           = db.Column(db.String(120), unique = True)
    aka             = db.Column(db.String(120), unique = True)
    phone           = db.Column(db.String(120), unique = True)
    shippingAddress = db.Column(db.String(120), unique = True)
    billingAddress  = db.Column(db.String(120), unique = True)
    ageGroup        = db.Column(db.String(120), unique = True)
    gender          = db.Column(db.String(120), unique = True)
    country         = db.Column(db.String(120), unique = True)
    dob             = db.Column(db.String(120), unique = True)
    #pref            = db.Column(db.String(1200), unique = True)

    def __init__(self, user, email, aka, phone, shippingAddress, billingAddress,
                    ageGroup, gender, country, dob):
        self.user               = user
        self.email              = email
        self.aka                = aka
        self.phone              = phone
        self.shippingAddress    = shippingAddress
        self.billingAddress     = billingAddress
        self.ageGroup           = ageGroup
        self.gender             = gender
        self.country            = country
        self.dob                = dob
        #self.pref               = pref

    def __repr__(self):
        return str(self.id) + ' - ' + str(self.user)

    def save(self):

        # inject self into db session    
        db.session.add ( self )

        # commit change and save the object
        db.session.commit( )

        return self 
