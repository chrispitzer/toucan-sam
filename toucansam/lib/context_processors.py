from django.conf import settings

CONTEXT_DICT = dict(
        CSS_COLORS=['gold', 'Fuchsia', 'hotpink', 'lime', 'orangered', 'red', 'sienna', 'darkorchid']
)

def config(request):
    return CONTEXT_DICT
