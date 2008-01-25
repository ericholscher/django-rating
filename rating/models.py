"""
Models for generic rating.

"""
import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# FloatField was renamed to DecimalField in r5302.
try:
    from django.db.models import FloatField as DecimalField
except ImportError:
    from django.db.models import DecimalField

# Generic relations were moved in r5172
try:
    from django.contrib.contenttypes import generic
except ImportError:
    import django.db.models as generic

from rating.managers import RatedItemManager, RateManager


class RatedItem(models.Model):
    """
    Rate info for an object.

    """
    rate_average = DecimalField(_('rating average'), max_digits=7,
                                decimal_places=2)
    rate_count = models.PositiveIntegerField(_('rating count'))

    last_rated_on = models.DateTimeField(_('last rate on'), editable=False,
                                         null=True)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey('content_type', 'object_id')

    objects = RatedItemManager()

    class Meta:
        verbose_name = _('rated item')
        verbose_name_plural = _('rated items')
        unique_together = (('content_type', 'object_id'),)

    def __str__(self):
        return _('Rating for %s') % self.object

    def add_rate(self, value, user):
        now = datetime.datetime.now()
        self.rates.create(rated_object=self, rate=value, user=user, date=now)
        self.rate_count += 1
        self.rate_average = Rate.objects.rate_average(self.object)
        self.last_rate_on = now
        self.save()
        return self

    def get_average(self):
        return '%.1f' % self.rate_average

    def save(self):
        if not self.id:
            self.rate_count = 0
            self.rate_average = 0
        super(RatedItem, self).save()


class Rate(models.Model):
    """
    Rate detail.

    """
    rated_object = models.ForeignKey('RatedItem', related_name='rates')
    user = models.ForeignKey(User, verbose_name=_('user'), null=True,
                             blank=True)
    rate = models.PositiveSmallIntegerField(_('rating value'))
    date = models.DateTimeField(_('rated on'), editable=False)

    objects = RateManager()

    def save(self):
        if not self.id:
            self.date = datetime.datetime.now()
        super(Rate, self).save()
