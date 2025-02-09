from datetime import datetime, timedelta
import re

def parse_duration(duration_str):
    """Parses '8h' or '75m' and returns a timedelta object."""
    match = re.match(r"(\d+)([hm])", duration_str.strip().lower())

    if not match:
        raise ValueError("Invalid duration format. Use '8h' or '75m'.")

    value, unit = int(match.group(1)), match.group(2)

    if unit == "h":
        delta = timedelta(hours=value)
    elif unit == "m":
        delta = timedelta(minutes=value)

    return delta

def recurseprint(json, name, field, i):
    """Recursively prints all objects in json["field"] nested structures"""
    if len(json) != 0:
        for each in json[field]:
            recurseprint(each[field], name, field, i+1)
            print(each)
    return
