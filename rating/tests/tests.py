# -*- coding: utf-8 -*-
r"""
>>> from django.contrib.auth.models import User
>>> from rating.tests.models import Movie
>>> from rating.models import RatedItem, Rate

>>> user = User.objects.create(username='gonz')
>>> user
<User: gonz>

>>> m = Movie.objects.create(name="Fear and Loathing in Las Vegas")
>>> m
<Movie: Fear and Loathing in Las Vegas>

>>> RatedItem.objects.add_rate(object=m, value=3, user=user)
<RatedItem: Rating for Fear and Loathing in Las Vegas>

>>> RatedItem.objects.add_rate(object=m, value=2, user=user)
<RatedItem: Rating for Fear and Loathing in Las Vegas>

>>> RatedItem.objects.add_rate(object=m, value=5, user=user)
<RatedItem: Rating for Fear and Loathing in Las Vegas>

>>> r = RatedItem.objects.get_for_object(m)
>>> r
<RatedItem: Rating for Fear and Loathing in Las Vegas>

>>> r.rate_average
3.3333333333333335

"""
