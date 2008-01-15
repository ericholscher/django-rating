"""
Models for generic rating.

"""
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Generic relations were moved in Django revision 5172
try:
    from django.contrib.contenttypes import generic
except ImportError:
    import django.db.models as generic


class RatedItem(models.Model):
    """
    Rate for a object by a user.

    """
    user = models.ForeignKey(User)
    rate = models.PositiveSmallIntegerField(_('rating'))

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('rated item')
        verbose_name_plural = _('rated items')
        unique_together = (('user', 'content_type', 'object_id'),)

    def __str__(self):
        dict = {'object': self.object, 'rate': self.rate, 'user': self.user}
        return _('%(object)s rated %(rate)s by %(user)s') % dict
