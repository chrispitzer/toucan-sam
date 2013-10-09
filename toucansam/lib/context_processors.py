from django.conf import settings

def config(request):
    return {
        "CSS_COLORS": settings.TOUCAN_COLORS
    }
