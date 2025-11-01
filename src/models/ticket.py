from enum import Enum
from src.utils.db_utils import db
import uuid
from datetime import datetime

class TicketStatus(Enum):
    RESERVED = "reserved"
    PAID = "paid"
    EXPIRED = "expired"


class Ticket(db.Model):
    __tablename__ = "tickets"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("users.id"))
    event_id = db.Column(db.String, db.ForeignKey("events.id"))
    status = db.Column(db.String, default="reserved")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="tickets")
    event = db.relationship("Event", backref="tickets")