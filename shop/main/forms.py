from django import forms
from main.models import Order
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

class OrderForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(attrs={'class': 'phone-number'}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'address','city', 'telegram_name']


    def __init__(self, *args, **kwargs):
        initial_data = kwargs.get('initial', {})
        if 'first_name' in initial_data:
            kwargs.setdefault('initial', {})['first_name'] = initial_data['first_name']
        if 'last_name' in initial_data:
            kwargs.setdefault('initial', {})['last_name'] = initial_data['last_name']
        if 'email' in initial_data:
            kwargs.setdefault('initial', {})['email'] = initial_data['email']
        super(OrderForm, self).__init__(*args, **kwargs)

