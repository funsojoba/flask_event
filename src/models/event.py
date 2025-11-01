from src.utils.db_utils import db
import uuid
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import composite
from src.models.venue import Venue

class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    total_tickets = db.Column(db.Integer, nullable=False)
    tickets_sold = db.Column(db.Integer, default=0)
    # venue = db.Column(JSONB, nullable=False)  # { "address": "...", "lat": 6.5, "lng": 3.4 }
    
    venue_address = db.Column(db.String(255), nullable=False, server_default='Unknown')
    venue_latitude = db.Column(db.Float, nullable=False)
    venue_longitude = db.Column(db.Float, nullable=False)

    venue = composite(Venue, venue_address, venue_latitude, venue_longitude)