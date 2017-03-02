from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget
from django.contrib.admin.templatetags.admin_static import static
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.conf import settings

__all__ = [
    'AdminHStoreWidget',
]


class AdminHStoreWidget(AdminTextareaWidget):
    """
    Base admin widget class for default-admin and grappelli-admin widgets
    """
    admin_style = 'default'

    @property
    def media(self):
        internal_js = [
            "core/js/underscore-min.js",
            "core/js/hstore-widget.js"
        ]

        js = [static(path) for path in internal_js]

        return forms.Media(js=js)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}
        # it's called "original" because it will be replaced by a copy
        attrs['class'] = 'hstore-original-textarea'

        # get default HTML from AdminTextareaWidget
        html = super(AdminHStoreWidget, self).render(name, value, attrs)

        # prepare template context
        template_context = Context({
            'field_name': name,
            'STATIC_URL': settings.STATIC_URL
        })
        # get template object
        template = get_template('hstore_%s_widget.html' % self.admin_style)
        # render additional html
        additional_html = template.render(template_context)

        # append additional HTML and mark as safe
        html = html + additional_html
        html = mark_safe(html)

        return html


class AdminJSONWidget(AdminTextareaWidget):
    admin_style = 'default'

    @property
    def media(self):
        internal_js = [
            "core/js/json-widget.js",
            "core/js/pretty-json.min.js"
        ]

        js = [static(path) for path in internal_js]

        return forms.Media(js=js)

    def render(self, name, value, attrs=None):
        if attrs is None:
            attrs = {}

        attrs['class'] = 'json-original-textarea'
        html = super().render(name, value, attrs)

        # prepare template context
        template_context = Context({
            'field_name': name,
            'STATIC_URL': settings.STATIC_URL
        })

        template = get_template('json_%s_widget.html' % self.admin_style)
        additional_html = template.render(template_context)

        html = html + additional_html
        html = mark_safe(html)

        return html
