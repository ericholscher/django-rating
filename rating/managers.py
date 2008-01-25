"""
Custom Managers for generic rating models.

"""
from django.db.models import Manager
from django.contrib.contenttypes.models import ContentType

from rating.utils import get_target_for_object


class RatedItemManager(Manager):
    def get_for_object(self, object):
        ctype_id, obj_id = get_target_for_object(object)
        try:
            return self.get(content_type__pk=ctype_id,
                            object_id=obj_id)
        except:
            return None

    def add_rate(self, object, value, user):
        rated_item = self.get_for_object(object)
        if not rated_item:
            rated_item = self.create(object=object)
        return rated_item.add_rate(value, user)


class RateManager(Manager):
    def rate_average(self, object):
        ctype = ContentType.objects.get_for_model(object)
        rate_items = list(self.filter(rated_object__content_type__pk=ctype.id,
                                      rated_object__object_id=object._get_pk_val()))
        return reduce(lambda x, y: x+y, [rate_item.rate for rate_item in rate_items]) / float(len(rate_items))
