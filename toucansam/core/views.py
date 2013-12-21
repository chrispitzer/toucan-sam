import json
import os
import re
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from core.models import Song, Gig, SetList, SetItem
from core.templatetags.toucan import randocolor
from lib.decorators import template

from django.shortcuts import get_object_or_404, redirect


class MobileTemplateView(TemplateView):
    is_mobile = False

    def is_request_mobile(self, request):
        """
        Snipped pulled from https://djangosnippets.org/snippets/2001/
        """
        if 'mobile' in request.GET:
            return request.GET.get('mobile', 'no').lower() in ('yes', 'true', '1')

        is_mobile = False

        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']

            # Test common mobile values.
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront)"
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)

            if match:
                is_mobile = True
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if request.META.has_key('HTTP_ACCEPT'):
                    http_accept = request.META['HTTP_ACCEPT']

                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog = re.compile(pattern, re.IGNORECASE)

                    match = prog.search(http_accept)

                    if match:
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
                                    "avan", "benq", "bird", "blac", "blaz", "brew",
                                    "cell", "cldc", "cmd-", "dang", "doco", "eric",
                                    "hipt", "inno", "ipaq", "java", "jigs", "kddi",
                                    "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
                                    "maui", "maxo", "midp", "mits", "mmef", "mobi",
                                    "mot-", "moto", "mwbp", "nec-", "newt", "noki",
                                    "xda",  "palm", "pana", "pant", "phil", "play",
                                    "port", "prox", "qwap", "sage", "sams", "sany",
                                    "sch-", "sec-", "send", "seri", "sgh-", "shar",
                                    "sie-", "siem", "smal", "smar", "sony", "sph-",
                                    "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
                                    "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
                                    "wapi", "wapp", "wapr", "webc", "winw", "winw",
                                    "xda-",)

                test = user_agent[0:4].lower()
                if test in user_agents_test:
                    is_mobile = True

        return is_mobile

    def dispatch(self, request, *args, **kwargs):
        self.is_mobile = self.is_request_mobile(request)
        return super(MobileTemplateView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        templates = super(MobileTemplateView, self).get_template_names()
        if self.is_mobile:
            templates = [os.path.join('mobile', t) for t in templates]
        return templates


class SongListView(MobileTemplateView):
    template_name = "song_list.html"

    def get_context_data(self, **kwargs):
        context = super(SongListView, self).get_context_data(**kwargs)
        context['songs'] = Song.active_objects.all()
        context['set_list_id'] = "new"
        return context


class SetListView(TemplateView):
    template_name = "set_list.html"

    def get_context_data(self, set_list_id, **kwargs):
        context = super(SetListView, self).get_context_data(**kwargs)
        if set_list_id == "new":
            set_list = SetList()
        else:
            set_list = get_object_or_404(SetList, id=set_list_id)

        songs = Song.active_objects.exclude(set_lists=set_list)
        if not set_list.show_proposed:
            songs = songs.exclude(proposed=True)
        context.update({
            "songs": songs,
            "set_list_id": set_list_id,
            "set_list": set_list
        })
        return context


    def post(self, request, set_list_id, **kwargs):
        if request.POST['toggle_proposed']:
            set_list = get_object_or_404(SetList, id=set_list_id)
            set_list.show_proposed = not set_list.show_proposed
            set_list.save()
        return redirect(reverse("set_list", args=[set_list_id]))


class AjaxException(Exception):
    def __init__(self, msg):
        self.message = msg

    def __unicode__(self):
        return unicode(self.message)


class AjaxView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        try:
            content = super(AjaxView, self).dispatch(request, *args, **kwargs)
        except AjaxException, e:
            content = {'error': unicode(e)}
        return HttpResponse(json.dumps(content), content_type="application/json")


class SetListAjax(AjaxView):

    def post(self, request, set_list_id):
        gig_name = request.POST["gig_name"]
        response_data = '{}'

        if set_list_id == "new":
            if SetList.objects.filter(gig__name=gig_name).exists():
                raise AjaxException("A set named '{0}' already exists.  Be more creative.".format(gig_name))
            else:
                set_list = SetList.objects.create(gig=Gig.objects.create())
                response_data = json.dumps({
                    'refresh': reverse("set_list", kwargs={"set_list_id": set_list.id})
                })
        else:
            set_list = get_object_or_404(SetList, id=set_list_id)

        set_list.gig.name = gig_name
        set_list.gig.save()

        set_list.songs.clear()
        for song_order, song_id in enumerate(request.POST.getlist('songs[]')):
            song = Song.objects.get(id=song_id)
            SetItem.objects.create(set_list=set_list, song=song, order=song_order)

        return response_data


class SetListSecondsjaxView(AjaxView):
    def get(self, request, set_list_id):
        if set_list_id == "new":
            return "0:00"
        else:
            set_list = get_object_or_404(SetList, id=set_list_id)

        return str(set_list.run_time)


class SetListList(TemplateView):
    template_name = "set_list_list.html"

    def get_context_data(self, **kwargs):
        context = super(SetListList, self).get_context_data(**kwargs)
        context['set_list_list'] = SetList.objects.all()
        return context

set_list_list = SetListList.as_view()


class SongView(TemplateView):
    template_name = "song.html"

    def get_context_data(self, song_id, **kwargs):
        context = super(SongView, self).get_context_data(**kwargs)
        context['song'] = get_object_or_404(Song, id=song_id)
        return context

    def post(self, request, song_id):
        if request.POST['accept_proposed']:
            song = get_object_or_404(Song, id=song_id)
            song.proposed = False
            song.save()
        return redirect("song", song_id)


class CheatSheetView(TemplateView):
    template_name = "cheat_sheet.html"

    def get_context_data(self, set_list_id=None, **kwargs):
        context = super(CheatSheetView, self).get_context_data(**kwargs)
        if set_list_id is not None:
            set_list = get_object_or_404(SetList, id=set_list_id)
            songs = set_list.ordered_songs
        else:
            songs = Song.active_objects.order_by('title')
        column_count = int(self.request.GET.get('columns', 2))
        row_count = len(songs) / column_count
        remainder = len(songs) % column_count
        columns = []
        start = 0
        for i in range(column_count):
            end = start + row_count
            if remainder > 0:
                end += 1
                remainder -= 1
            columns.append(songs[start:end])
            start = end

        context['column_width'] = (1./column_count) * 100
        context['song_columns'] = columns
        return context


class RandoColor(AjaxView):

    def get(self, request):
        return randocolor()