from app import db
from datetime import datetime, timedelta


class Auto(db.Model):
    auto_id = db.Column(db.Integer, primary_key=True)
    name_auto = db.Column(db.String(128))
    description = db.Column(db.Text)
    rent_price = db.Column(db.Float)
    transmission = db.Column(db.Boolean)
    img_url = db.Column(db.String(128))
    img_url2 = db.Column(db.String(128))
    img_url3 = db.Column(db.String(128))
    img_url4 = db.Column(db.String(128))
    rent_status = db.Column(db.String(128), default = 'Арендовать')
    car_availability = db.Column(db.String(128), default = 'Свободен')

    

class RentHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auto_id2 = db.Column(db.Integer)
    beginning_date = db.Column(db.String(128))
    end_date = db.Column(db.String(128))
    total_price = db.Column(db.Float)
    total_time = db.Column(db.Integer)


class RentJournal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    bookings_number = db.Column(db.Integer, default = 0)
    total_minute =  db.Column(db.String(128))
    total_second = db.Column(db.String(128))
    total_amount = db.Column(db.Float)
    photo = db.Column(db.String(128))
    
    


    

