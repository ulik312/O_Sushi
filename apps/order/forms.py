from django import forms

from .models import Order


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата получения заказа'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = [
            'name', 'last_name', 'address', 'phone', 'person',
            'payment', 'branch', 'delivery_type', 'order_date', 'comment'
        ]


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'