from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django.utils.timezone import now
from django.views import generic

from heaven.core.mixins import NavigationMixin
from .models import Escort, Category

# Create your views here.
class LandingPage(generic.TemplateView):
    template_name = 'landing/landing.html'

    def get_context_data(self, **kwargs):
        kwargs['categories'] = Category.objects.all()

        escorts = Escort.objects.published()
        kwargs['featured'] = escorts.featured()[:6]
        kwargs['most_popular'] = escorts.most_popular()[:8]
        kwargs['most_recent'] = escorts.most_recent()[:8]

        return super().get_context_data(**kwargs)

class BaseEscortListView(generic.ListView):
    template_name = 'landing/category.html'
    model = Escort
    paginate_by = 30
    active_menu = None

    def get_queryset(self):
        return super().get_queryset().published()

    def get_context_data(self, **kwargs):
        kwargs['categories'] = Category.objects.all()
        kwargs['active_menu'] = self.active_menu
        return super().get_context_data(**kwargs)

class GalleryPageListView(BaseEscortListView):

    def get_queryset(self):
        return super().get_queryset().published().order_by('name')


class EscortFeaturedListView(BaseEscortListView):
    active_menu = 'featured'

    def get_queryset(self):
        return super().get_queryset().published().featured()[:20]


class EscortPopularListView(BaseEscortListView):
    active_menu = 'popular'

    def get_queryset(self):
        return super().get_queryset().most_popular()[:20]


class EscortRecentListView(BaseEscortListView):
    active_menu = 'most_recent'

    def get_queryset(self):
        return super().get_queryset().most_recent()[:20]

class AvailableTodayPage(BaseEscortListView):
    active_menu = 'available_today'

    def get_queryset(self):
        return super().get_queryset().available_today()[:20]

class EscortCategoryListView(BaseEscortListView):
    category = None

    def get_queryset(self):
        slug = self.kwargs.get('slug', None)
        escorts = super().get_queryset()

        if slug:
            self.category = get_object_or_404(Category, slug=slug)
            escorts = escorts.filter(category=self.category)

        return escorts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_menu'] = self.category.slug
        return context

class EscortDetailView(generic.DetailView):
    model = Escort
    context_object_name = 'escort'
    template_name = 'landing/escort.html'

    def get_object(self, queryset=None):
        try:
            obj = (Escort.objects
                   .published()
                   .select_related('girl')
                   .get(slug=self.kwargs['slug'], published=True))

        except Escort.DoesNotExist:
            raise Http404('Escort does not exists')
        else:
            return obj

    def get_context_data(self, **kwargs):
        kwargs['categories'] = Category.objects.all()
        return super().get_context_data(**kwargs)