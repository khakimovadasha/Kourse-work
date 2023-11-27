from django import  forms
from django.forms import ClearableFileInput

from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm


class SignInForm(AuthenticationForm,forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user


class CustomUserForm(UserChangeForm):
    img = forms.ImageField(widget=ClearableFileInput(attrs={'accept': 'image/*'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'bio', 'img', 'email')