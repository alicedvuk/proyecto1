from django.core.cache import cache
from django import template
from django.core.urlresolvers import Resolver404
from django.template import TemplateSyntaxError

register = template.Library()


class GetParametersNode(template.Node):
    """
    Renders current get parameters except for the specified parameter
    """

    def __init__(self, field):
        self.field = field

    def render(self, context):
        request = context['request']
        getvars = request.GET.copy()

        if self.field in getvars:
            del getvars[self.field]

        if len(getvars.keys()) > 0:
            get_params = "%s&" % getvars.urlencode()
        else:
            get_params = ''

        return get_params


class ResolveNode(template.Node):
    def __init__(self, path, asvar):
        self.path = path
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import resolve

        path = self.path.resolve(context)

        try:
            resolved = resolve(path)
        except Resolver404:
            return ''

        if self.asvar:
            context[self.asvar] = resolved
            return ''

        return '%s:%s' % (resolved.namespace, resolved.url_name)


@register.assignment_tag(name='cache_get')
def do_cache_get(key):
    return cache.get(key)


@register.tag('urlparams')
def do_urlparams(parser, token):
    """
    {% urlparams exclude_args %}
    """

    args = token.split_contents()
    if len(args) < 2:
        raise template.TemplateSyntaxError(
            "urlparams tag takes at least 1 argument")
    return GetParametersNode(args[1].strip())


@register.assignment_tag(name='bootstrap_alert_css_class')
def do_bootstrap_alert_css_class(message):
    if message.level_tag == 'error':
        return 'alert-danger'
    else:
        return 'alert-%s' % message.level_tag


@register.tag(name='resolve')
def do_resolve(parser, token):
    """
    Tag can be used for resolving URL paths to the corresponding view functions

    {% resolve '/some/path/' as urlname %}

        it returns a ResolverMatch object

        urlname.func
        urlname.args
        urlname.kwargs
        urlname.url_name
        urlname.app_name
        urlname.namespace
        urlname.namespaces
        urlname.view_name

    {% resolve '/some/path/' %}

        will render 'namespace:url_name'

    """

    bits = token.split_contents()
    asvar = None

    if len(bits) not in (2, 4):
        raise TemplateSyntaxError("'%s' use one or two arguments"
                                  " (url path)" % bits[0])

    if len(bits) == 4 and bits[-2] == 'as':
        asvar = bits[-2]

    path = parser.compile_filter(bits[1])
    print(path, asvar)
    return ResolveNode(path, asvar)
