from django.contrib.contenttypes.models import ContentType


def get_target_for_object(object, as_str=False):
    ctype = ContentType.objects.get_for_model(object)
    target_list = [ctype.id, object._get_pk_val()]
    if as_str:
        return ':'.join(target_list)
    return target_list
