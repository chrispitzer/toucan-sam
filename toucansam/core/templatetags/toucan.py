from datetime import time, timedelta
import json
import random
from django.conf import settings
from django.template.defaulttags import register

@register.simple_tag()
def randocolor():
    return random.choice(settings.TOUCAN_COLORS)

@register.filter(name="range")
def range_tpl(num):
    return range(int(num))

@register.filter
def json_dump(data):
    return json.dumps(data)
