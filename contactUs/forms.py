from django.forms import ModelForm, Textarea

from .models import Contact


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = [
            'fullname',
            'email',
            'message',
        ]
        widgets = {
            'message': Textarea,
        }

