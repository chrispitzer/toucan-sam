class Http500(Exception): pass

class HttpRedirect(Exception):
    def __init__(self, *args, **kwargs):
        if not 'url' in kwargs:
            raise Http500("You can't use this exception without a url")
        self.url = kwargs.pop('url')

