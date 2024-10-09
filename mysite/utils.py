"""Utility function for defining timezone offset"""
import pytz
from datetime import datetime

def get_time_zone_offset(time_zone: str) -> int:
    """Get the UTC offset for a given time zone."""
    try:
        # Get the timezone object
        tz = pytz.timezone(time_zone)
        # Get the current time in UTC
        now_utc = datetime.now(pytz.utc)
        # Get the local time in the specified timezone
        local_time = now_utc.astimezone(tz)
        # Calculate the offset in hours
        offset = local_time.utcoffset().total_seconds() / 3600
        return int(offset)
    except Exception as e:
        print(f"Error getting offset for time zone {time_zone}: {e}")
        return 0  # Return 0 if there's an error
