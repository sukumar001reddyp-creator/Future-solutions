from datetime import datetime
from app import db

class QuoteRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    incoterms = db.Column(db.String(50), nullable=False)
    pickup = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=True)
    volume = db.Column(db.Float, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ShipmentTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    mode_of_shipment = db.Column(db.String(50), nullable=True)
    shipping_line = db.Column(db.String(100), nullable=True)
    vessel = db.Column(db.String(100), nullable=True)
    container_no = db.Column(db.String(100), nullable=True)
    etd = db.Column(db.String(50), nullable=True)
    eta = db.Column(db.String(50), nullable=True)
    cargo_description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)