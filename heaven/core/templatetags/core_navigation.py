from django import template
from django.template import Library

register = Library()


class ActiveItemNode(template.Node):
    def __init__(self, active_item, active_name):
        self.active_item = template.Variable(active_item)
        self.active_name = template.Variable(active_name)

    def render(self, context):
        if self.active_item.resolve(context) in context.get('active_items', []):
            return self.active_name.resolve(context)
        return ''


@register.tag
def is_active(parser, token):
    """
    Utility to get the active section in a navigation, for example::

        {% is_active 'account:stream' as 'selected'%}

    will render 'selected' if in the context the `active_items` variable is set
    as: ['account:stream']
    """

    try:
        tag_name, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires arguments" % token.contents.split()[0])

    options = args.split(' as ', 1)

    if len(options) == 1:
        active_item, active_name = options[0], '"active"'
    elif len(options) == 2:
        active_item, active_name = options[0], options[1]
    else:
        raise template.TemplateSyntaxError("%r tag had invalid arguments" % tag_name)

    return ActiveItemNode(active_item=active_item, active_name=active_name)
