from datetime import time
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

@register.filter
def format_seconds(seconds):
    try:
        seconds = int(seconds)
    except:
        return seconds
    hours = seconds / (60*60)
    seconds %= 60 * 60
    minutes = seconds / 60
    seconds %= 60

    # truncate hours if zero, then minute if zero
    timelist = [hours, minutes, seconds]
    while timelist[0] == 0 and len(timelist) > 1:
        timelist = timelist[1:]

    #turn ints to strings -- everything but the first one gets leading zeroes
    timestrings = []
    for t in timelist:
        if t == timelist[0]:
            t = str(t)
        else:
            t = format(t, '02d')
        timestrings.append(t)

    return ":".join(timestrings)