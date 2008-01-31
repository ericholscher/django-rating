from django import template
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template


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


class RateFormNode(template.Node):
    def __init__(self, object_name):
        self.object_name = object_name

    def render(self, context):
        object = template.resolve_variable(self.object_name, context)
        ctype_id, obj_id = get_target_for_object(object)
        t = get_template('rating/rating_form.html')
        c = context
        c.update({'ctype_id': ctype_id, 'obj_id': obj_id})
        return t.render(c)
                                                 


@register.tag('rating_form')
def do_rating_form(parser, token):
    """
    Syntax::

        {% rating_form for [object] %}

    Example usage::

        {% rating_form for program %}

    """
    tokens = token.contents.split()
    tag_name = tokens[0]
    if len(tokens) != 3:
        raise template.TemplateSyntaxError, '%r tag requires 3 arguments' % tag_name
    if tokens[1] != 'for':
        raise template.TemplateSyntaxError, "%r tag's second " \
                                            "argument must be 'for'" % tag_name
    return RateFormNode(object_name=tokens[2])
