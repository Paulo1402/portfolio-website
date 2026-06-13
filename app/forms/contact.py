from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(
        label=_("Name"),
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Your name"),
            }
        ),
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Your email"),
            }
        ),
    )
    message = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": _("Write your message"),
                "rows": 3,
            }
        ),
    )
