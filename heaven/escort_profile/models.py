from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.text import slugify
from heaven.girls.models import Girl
from heaven.core.utils import build_absolute_uri
from ckeditor.fields import RichTextField
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=False)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'category_escorts', None, {'slug': self.slug}

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.slug)
        super().save(**kwargs)


class EscortQueryset(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def most_popular(self):
        return self.filter(popular=True)

    def most_recent(self):
        return self.filter().order_by('-created')

    def published(self):
        return self.filter(published=True)
        
    def available_today(self):
        return self.filter(available_today=True)

class EscortManager(models.Manager.from_queryset(EscortQueryset)):
    def get_queryset(self):
        return super().get_queryset().select_related('girl', 'category')


class Escort(models.Model):
    girl = models.OneToOneField(Girl, verbose_name='escortgirl', blank=True, null=True)
    #girl = models.CharField(max_length=140, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True)

    slug = models.SlugField(unique=True)
    name = models.CharField(unique=True, max_length=140)
    photo = models.ImageField(
        upload_to='london-escort-agency/%Y/%m/%d',
        verbose_name='Pic 1',
        blank=True,
        null=True
    )
    photo_1 = models.ImageField(
        upload_to='london-escort-agency/%Y/%m/%d',
        verbose_name='Pic 2',
        blank=True,
        null=True
    )
    photo_2 = models.ImageField(
        upload_to='london-escort-agency/%Y/%m/%d',
        verbose_name='Pic 3',
        blank=True,
        null=True
    )
    photo_3 = models.ImageField(
        upload_to='london-escort-agency/%Y/%m/%d',
        verbose_name='Pic 4',
        blank=True,
        null=True
    )
    photo_4 = models.ImageField(
        upload_to='london-escort-agency/%Y/%m/%d',
        verbose_name='Pic 5',
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)
    rates = RichTextField(blank=True)
    caption = models.CharField(max_length=140, blank=True)
    tagline = models.CharField(max_length=140, blank=True)
    age = models.PositiveIntegerField(blank=True)
    measurements = models.CharField(max_length=140, blank=True)
    dress_size = models.CharField(max_length=140, blank=True)
    complexion = models.CharField(max_length=140, blank=True)
    build = models.CharField(max_length=140, blank=True)
    height = models.CharField(max_length=140, blank=True)
    hair = models.CharField(max_length=140, blank=True)
    eye = models.CharField(max_length=140, blank=True)
    nationality = models.CharField(max_length=140, blank=True)
    languages = models.CharField(max_length=140, blank=True)
    sexual_orientation = models.CharField(max_length=140, blank=True)
    incall_outcall = models.CharField(max_length=140, blank=True)

    background = models.ImageField(blank=True)
    primary_color = models.CharField(max_length=6, blank=True)
    background_color = models.CharField(max_length=6, blank=True)

    redirect = models.URLField(max_length=140, blank=True)
    allow_follow = models.BooleanField(default=True)
    published = models.BooleanField(default=True, db_index=True)

    featured = models.BooleanField(default=False, db_index=True)
    popular = models.BooleanField(default=False, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    available_today = models.BooleanField(default=False, db_index=True)

    objects = EscortManager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.verbose_name

    @property
    def verbose_name(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'escort_profile', None, {'slug': self.slug}

    def get_canonical_url(self, params: dict = None) -> str:
        return build_absolute_uri(self.get_absolute_url(), params=params)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(**kwargs)

    """ Informative name for mode """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.title, public_id)