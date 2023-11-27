from django import forms


class CardAddProductForm(forms.Form): #card - опечатка
    quantity = forms.IntegerField(min_value=1 ) #позволяет пользователю выбирать кол-во товара
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)