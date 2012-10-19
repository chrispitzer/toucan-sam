from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.urlresolvers import reverse, NoReverseMatch
import warnings
from copy import deepcopy


class SetRemoteAddrMiddleware(object):
    def process_request(self, request):
        if request.META.has_key('HTTP_X_REAL_IP'):
            request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
        if not request.META.has_key('REMOTE_ADDR'):
            request.META['REMOTE_ADDR'] = '1.1.1.1' # This will place a valid IP in REMOTE_ADDR but this shouldn't happen


from lib.exceptions import HttpRedirect
class HttpRedirectCatchMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, HttpRedirect):
            return HttpResponseRedirect(exception.url)


class LoginRequiredMiddleware(object):
    def __init__(self, *args, **kwargs):
        try:
            LOGIN_URL = settings.LOGIN_URL
        except ImportError:
            warnings.warn("missing LOGIN_URL in settings", ImportWarning)
            LOGIN_URL = '/login/'

        try:
            admin_login_url = reverse('admin:index')
        except NoReverseMatch:
            admin_login_url = None

        try:
            ALLOWED_URLS = deepcopy(settings.ALLOWED_URLS) + [ LOGIN_URL ]
        except ImportError:
            ALLOWED_URLS = [ LOGIN_URL]
        self.ALLOWED_URLS = ALLOWED_URLS

        try:
            self.ALLOWED_URLS.append(reverse('admin:index'))
        except NoReverseMatch: pass

    def process_request(self, request):
        if settings.DEBUG and request.path_info.startswith(settings.MEDIA_URL):
            return
        if request.path_info in self.ALLOWED_URLS:
            return
        if not request.user.is_authenticated():
            return HttpResponseRedirect(settings.LOGIN_URL)


class HandlePutMethodMiddleware(object):
    def process_request(self, request):
        request.PUT = {}
        if request.method != "PUT":
            return

        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'

        request.PUT = request.POST
        request.POST = {}
