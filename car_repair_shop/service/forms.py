from django import forms
from .models import Order, TimeSlot


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        # exclude = ('service', )
        fields = ['service', 'customer', 'box', 'time_slot']
        # fields = '__all__'
        field_order = ['service', 'customer', 'box', 'time_slot']
        # widgets = {
        #     'pub_date': forms.DateInput(attrs={'type': 'date'})
        # }

    def __init__(self, *args, **kwargs):
        super(CreateOrderForm, self).__init__(*args, **kwargs)
        # self.fields['time_slot'].queryset = TimeSlot.objects.none()
