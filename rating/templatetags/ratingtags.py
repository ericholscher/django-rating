from django import template
from django.contrib.contenttypes.models import ContentType


from rating.models import *
from rating.utils import get_target_for_object


register = template.Library()


class GetRatingNode(template.Node):
    def __init__(self, object_name, var_name):
        self.object_name, self.var_name = object_name, var_name

    def render(self, context):
        object = template.resolve_variable(self.object_name, context)
        rating = RatedItem.objects.get_for_object(object)
        context[self.var_name] = rating
        return ''


@register.tag('get_rating')
def do_get_rating(parser, token):
    """
    Syntax::

        {% get_rating for [object] as [varname] %}

    Example usage::

        {% get_rating for program as program_rating %}

    """
    tokens = token.contents.split()
    tag_name = tokens[0]
    if len(tokens) != 5:
        raise template.TemplateSyntaxError, '%r tag requires 5 arguments' % tag_name
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError, "%r tag's second " \
                                            "argument must be 'for'" % tag_name
    if tokens[3] != 'as':
        raise template.TemplateSyntaxError, "%r tag's fourth " \
                                            "argument must be 'as'" % tag_name
    return GetRatingNode(object_name=tokens[2], var_name=tokens[4])


class RateLinkNode(template.Node):
    def __init__(self, object_name, rate):
        self.object_name, self.rate = object_name, rate

    def render(self, context):
        object = template.resolve_variable(self.object_name, context)
        ctype_id, obj_id = get_target_for_object(object)
        return 'rate/?target=%(ct_id)s:%(obj_id)s&rate=%(rate)s' % \
                                                           {'ct_id': ctype_id,
                                                            'obj_id': obj_id,
                                                            'rate': self.rate}


@register.tag('rate_link')
def do_rate_link(parser, token):
    """
    Syntax::

        {% rate_link for [object] [rate] %}

    Example usage::

        {% rate_link for program 2 %}

    """
    tokens = token.contents.split()
    tag_name = tokens[0]
    if len(tokens) != 4:
        raise template.TemplateSyntaxError, '%r tag requires 4 arguments' % tag_name
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError, "%r tag's second " \
                                            "argument must be 'for'" % tag_name
    try:
        rate = int(tokens[3])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag's third " \
                                            "argument must be an integer" % tag_name
    return RateLinkNode(object_name=tokens[2], rate=rate)
