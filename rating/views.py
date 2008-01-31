from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, Http404

from rating.models import RatedItem


# FIXME return a HttpResponse...
def rate(request):
    try:
        target, rate = request.POST['target'], request.POST['rate']
    except KeyError:
        raise Http404, 'falto param'
    content_type_id, object_id = target.split(':')
    try:
        object = ContentType.objects.get(pk=content_type_id).get_object_for_this_type(pk=object_id)
    except ObjectDoesNotExist:
        raise Http404, 'target vieno mal'
    rated_item = RatedItem.objects.add_rate(object, rate, request.user)
    return HttpResponse('', mimetype='text/plain')
