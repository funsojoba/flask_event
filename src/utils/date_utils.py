from datetime import datetime, timezone

def to_utc_aware(datetime_obj):
    if datetime_obj is None:
        return None
    # Parse ISO strings (handle trailing 'Z' as UTC)
    if isinstance(datetime_obj, str):
        date_str = datetime_obj
        if date_str.endswith("Z"):
            date_str = date_str[:-1] + "+00:00"
        try:
            datetime_obj = datetime.fromisoformat(s)
        except Exception:
            raise ValidationError("Invalid datetime format for start_time/end_time", "_schema")
    if isinstance(datetime_obj, datetime):
        if datetime_obj.tzinfo is None:
            return datetime_obj.replace(tzinfo=timezone.utc)
        return datetime_obj.astimezone(timezone.utc)
    raise ValidationError("Invalid datetime value for start_time/end_time", "_schema")
