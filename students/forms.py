from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import os
from django.core import validators
from django.core.files.images import get_image_dimensions

from .models import StudentProfile


class EditProfileForm(UserChangeForm):
    # password = None

    # def __init__(self, *args, **kwargs):
    #     super(EditProfileForm, self).__init__(*args, **kwargs)
    #     attrs = {'class': 'form-control', 'required': True}
    #     if self.instance and self.instance.pk:
    #         self.fields.pop('password', None)
    #     for field in self.fields.values():
    #         field.widget.attrs = attrs

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        pass
        # return self.initial["password"]

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class ImageUploadForm(forms.ModelForm):
    ALLOWED_TYPES = ['jpg', 'jpeg', 'png', 'gif']

    class Meta:
        model = StudentProfile
        fields = ['avatar']
        labels = {
            'avatar': 'Upload Profile Photo:',
        }
        help_texts = {
            'avatar': 'File formats: .jpg, .jpeg, .png, .gif',
        }


class AboutMeForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['description']
        labels = {
            'description': 'About Me:',
        }
        help_texts = {
            'description': 'Max: 120 Characters',
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 20, 'rows': 5}),
        }


class LoginForm(forms.Form):
        username = forms.CharField()
        password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email


# class PasswordResetForm(forms.Form):
    #    email = forms.EmailField()





'''

class ImageUploadForm(forms.ModelForm):
    ALLOWED_TYPES = ['jpg', 'jpeg', 'png', 'gif']

    class Meta:
        model = StudentProfile
        fields = ['avatar']
    
    
        def clean_avatar(self):
        avatar = self.cleaned_data.get('image', None)
        if not avatar:
            raise forms.ValidationError('Missing image file')
        try:
            extension = os.path.splitext(avatar.name)[1][1:].lower()
            if extension in self.ALLOWED_TYPES:
                return avatar
            else:
                raise forms.ValidationError('File types is not allowed')
        except Exception as e:
            raise forms.ValidationError('Can not identify file type')
            
            
            
        def clean_avatar(self):
         avatar = self.cleaned_data.get('profile_photo')
    
        try:
            # validate content type
            main, sub = avatar.content_type.split('/')
            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError(u'Please use a JPEG, '
                                                'GIF or PNG image.')
    
        except AttributeError:
            raise forms.ValidationError("please upload a photo")
            pass
    
        return avatar
    '''

























'''
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['avatar']


class ImageUploadForm(forms.Form):
    # user_profile_name = forms.CharField()
    profile_photo = forms.ImageField()
'''


















'''
class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = [
            'firstName', 'lastName',
            'email', 'password', 'password2',
            'street', 'apt', 'city', 'state', 'zipcode',
        ]
        labels = {
            'firstName': _('First Name'),
            'lastName': _('Last Name'),
            'password2': _('Confirm Password'),
            'Apt': _('Apt/House'),
            'zipcode': _('Zip Code'),
        }

        widgets = {
            'password': forms.PasswordInput,
            'password2': forms.PasswordInput
        }

        help_texts = {
            'password': _("Password must be 9 character's long & have a number")
        }

    def clean(self):
        cleaned_data = super().clean()
        password2 = self.cleaned_data.get('password2')
        print(password2)
        password = self.cleaned_data.get('password')
        print(password)

        if password2 != password:
            msg = "Passwords must match!"
            self.add_error('password', msg)
            # raise forms.ValidationError("Passwords must match!")

        min_length = 8
        if len(password) < min_length:
            msg = "Passwords must be 8 characters long!"
            self.add_error('password', msg)

        if not re.findall('\d', password):
            msg = "The password must contain at least 1 digit, 0-9!"
            self.add_error('password', msg)

        if not re.findall('[a-z]', password):
            msg = "The password must contain at least 1 lowercase letter, a-z!"
            self.add_error('password', msg)

        if not re.findall('[A-Z]', password):
            msg = "The password must contain at least 1 uppercase letter, A-Z!"
            self.add_error('password', msg)

        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            msg = "The password must contain at least 1 symbol!"
            self.add_error('password', msg)

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Students.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    '''






