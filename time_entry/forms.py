from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _

#does not used UserCreation form because i had done many changes.
class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(render_value=True,
                                   attrs={'autocomplete': 'new-password', 'class': 'form-control', }),

    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(render_value=True, attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        strip=False,

    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', "username",)
        field_classes = {'username': UsernameField}
        widgets = {'first_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'last_name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.TextInput(attrs={'class': 'form-control'}),
                   'username': forms.TextInput(attrs={'class': 'form-control'})}

    field_order = ['first_name', 'last_name', 'email', "profession", 'mobile', "username"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
