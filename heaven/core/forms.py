from django import forms
from django.template.loader import render_to_string


class WeightInput(forms.TextInput):
    template = 'weight_field_widget.html'

    def __init__(self, unit, *args, **kwargs):
        self.unit = unit
        super(WeightInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        widget = super(WeightInput, self).render(name, value, attrs=attrs)
        return render_to_string(self.template, {'widget': widget,
                                                'value': value,
                                                'unit': self.unit})


class WeightField(forms.DecimalField):
    def __init__(self, unit, decimal_places, widget=WeightInput, *args,
                 **kwargs):
        self.unit = unit
        step = 10 ** -decimal_places
        if isinstance(widget, type):
            widget = widget(unit=self.unit,
                            attrs={'type': 'number', 'step': step})
        super(WeightField, self).__init__(*args, widget=widget, **kwargs)
