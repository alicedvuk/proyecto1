from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'heaven.core'

    def ready(self):
        from . import signals # flake8: NOQA
