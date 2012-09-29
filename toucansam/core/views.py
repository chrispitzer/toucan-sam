# Create your views here.


def home(request):
    print "HOME"


def song_list(request):
    print "LIST"


def song(request, song_id):
    print "particular: %s" % song_id
