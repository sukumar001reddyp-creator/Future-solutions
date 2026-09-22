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