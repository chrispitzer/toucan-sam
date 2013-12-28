from datetime import time, timedelta
import json
import random
from django.conf import settings
from django.template.defaulttags import register

@register.simple_tag()
def randocolor():
    return random.choice(settings.TOUCAN_COLORS)

@register.filter(name="range")
def range_tpl(start, stop=None):
    try:
        start = int(start)
        stop = int(stop)
        return range(start, stop)
    except ValueError:
        return []

@register.filter
def json_dump(data):
    return json.dumps(data)
