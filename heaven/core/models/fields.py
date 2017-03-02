from django.core.exceptions import ImproperlyConfigured
from django.db.models import SubfieldBase, CharField, DecimalField
from django.utils import six

from heaven.core import forms


class NullCharField(CharField):
    """
    CharField that stores '' as None and returns None as ''
    Useful when using unique=True and forms. Implies null==blank==True.

    When a ModelForm with a CharField with null=True gets saved, the field will
    be set to '': https://code.djangoproject.com/ticket/9590
    This breaks usage with unique=True, as '' is considered equal to another
    field set to ''.
    """
    description = "CharField that stores '' as None and returns None as ''"

    def __init__(self, *args, **kwargs):
        if not kwargs.get('null', True) or not kwargs.get('blank', True):
            raise ImproperlyConfigured(
                "NullCharField implies null==blank==True")
        kwargs['null'] = kwargs['blank'] = True
        super(NullCharField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        return value if value is not None else ''

    def get_prep_value(self, value):
        prepped = super(NullCharField, self).get_prep_value(value)
        return prepped if prepped != "" else None

    def deconstruct(self):
        """
        deconstruct() is needed by Django's migration framework
        """
        name, path, args, kwargs = super(NullCharField, self).deconstruct()
        del kwargs['null']
        del kwargs['blank']
        return name, path, args, kwargs


class UppercaseCharField(CharField):
    def from_db_value(self, value, expression, connection, context):
        if isinstance(value, str):
            return value.upper()
        else:
            return value


class PositiveDecimalField(DecimalField):
    """
    A simple subclass of ``django.db.models.fields.DecimalField`` that
    restricts values to be non-negative.
    """

    def formfield(self, **kwargs):
        return super(PositiveDecimalField, self).formfield(min_value=0)


class WeightField(DecimalField):
    description = 'A field which stores a weight.'

    def __init__(self, verbose_name=None, unit=None, *args, **kwargs):
        self.unit = unit
        super(WeightField, self).__init__(verbose_name, *args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(WeightField, self).deconstruct()
        kwargs['unit'] = self.unit
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        defaults = {'unit': self.unit,
                    'decimal_places': self.decimal_places,
                    'form_class': forms.WeightField}
        defaults.update(kwargs)
        return super(WeightField, self).formfield(**defaults)
