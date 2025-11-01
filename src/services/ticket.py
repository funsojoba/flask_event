from src.utils.db_utils import db
from src.models.ticket import Ticket
from src.models.event import Event
from datetime import datetime, timedelta
from src.utils.celery_utils import celery

from src.serializers.ticket_serializer import ReserveTicketSerializer, TicketSerializer

@celery.task
def expire_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket and ticket.status == "reserved":
        ticket.status = "expired"
        db.session.commit()


def reserve_ticket(user_id, event_id):
    try:
        # Lock the row for this event during this transaction
        event = db.session.query(Event).with_for_update().get(event_id)

        if not event:
            return {"error": "Event not found"}, 404

        if event.tickets_sold >= event.total_tickets:
            return {"error": "Event sold out"}, 400

        # Create and reserve the ticket
        ticket = Ticket(user_id=user_id, event_id=event_id)
        db.session.add(ticket)
        event.tickets_sold += 1

        db.session.commit()

        # Schedule auto-expiry (e.g., 2 minutes)
        expire_ticket.apply_async((ticket.id,), countdown=120)

        return {"message": "Ticket reserved", "ticket_id": ticket.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def pay_for_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return {"error": "Ticket not found"}
    ticket.status = "paid"
    db.session.commit()
    return {"message": "Payment successful"}

def get_user_tickets(user_id):
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    serialized_tickets = [TicketSerializer().dump(ticket) for ticket in tickets]
    return {
        "tickets": serialized_tickets
    }