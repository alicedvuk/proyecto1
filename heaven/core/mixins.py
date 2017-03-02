from django.http import HttpResponsePermanentRedirect
from django.utils.http import urlquote


class RedirectDetailView:
    def redirect_absolute_url(self, request, obj):
        expected_path = obj.get_absolute_url()
        if expected_path != urlquote(request.path):
            return HttpResponsePermanentRedirect(expected_path)


class NavigationMixin:
    active_items = None

    def get_context_data(self, **kwargs):
        kwargs['active_items'] = self.active_items if self.active_items else []
        return super().get_context_data(**kwargs)
