from django.utils import simplejson

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from decimal import Decimal
import datetime


def template(template):

    def decorator(fn):
        def render(request, *args, **kwargs):
            context_data = fn(request, *args, **kwargs)
            if isinstance(context_data, HttpResponse):
                # View returned an HttpResponse like a redirect
                return context_data
            else:
                # For any other type of data try to populate a template
                return render_to_response(template,
                        context_data,
                        context_instance=RequestContext(request),
                    )
        return render

    return decorator


class BetterJSONEncoder(simplejson.JSONEncoder):
    """JSON encoder which understands decimals."""

    def default(self, obj):
        '''Convert object to JSON encodable type.'''
        if isinstance(obj, Decimal):
            return "%d" % obj
        if isinstance(obj, datetime.datetime):
            return obj.ctime()
        return simplejson.JSONEncoder.default(self, obj)


def jsonapi(fn):

    def to_json(request, *args, **kwargs):
        context_data = fn(request, *args, **kwargs)
        if isinstance(context_data, HttpResponse):
            return context_data
        return HttpResponse(simplejson.dumps(context_data, cls=DecimalFriendlyJSONEncoder),
                mimetype='application/json')
    return to_json


def notice_changed(*args):
    """Used for the Admin save_model object only. Pass fields you wish to see whether they're changed into as *args."""
    def decorator(func):
        def new(self, request, obj, form, change):
            changed = False
            for key, value in form.cleaned_data.items():
                if form.initial.get(key) != value:
                    if key in args:
                        changed = True
            return func(self, request, obj, form, change, changed)
        return new
    return decorator




def render(template, data, request):
    return render_to_response(template,
                              data,
                              context_instance=RequestContext(request))
