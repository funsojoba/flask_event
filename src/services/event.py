from src.utils.db_utils import db
from src.models.event import Event
from src.models.venue import Venue
from src.serializers.event_serializer import EventCreateSchema, EventResponseSchema
from marshmallow import ValidationError

def create_event(data):

    try:
        venue_data = data.pop("venue")
        venue = Venue(**venue_data)
        data["venue"] = venue

        event = Event(**data)
        db.session.add(event)
        db.session.commit()

        return {"id": event.id, "title": event.title}
    except Exception as e:
        return {"error": True, "errors": str(e)}

def list_events():
    events = Event.query.all()
    schema = EventResponseSchema(many=True)
    return schema.dump(events)


# def for_you()