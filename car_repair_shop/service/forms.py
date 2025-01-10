from django import forms
from .models import Order


class CreateOrderForm(forms.ModelForm):
    pass

    class Meta:
        model = Order
        # exclude = ('is_published', 'author')
        # widgets = {
        #     'pub_date': forms.DateInput(attrs={'type': 'date'})
        # }