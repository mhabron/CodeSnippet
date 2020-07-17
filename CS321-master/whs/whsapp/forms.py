import datetime
from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

    def widget_attrs(self, widget):
        return {
            **super().widget_attrs(widget),
            'autocapitalize': 'none',
            'autocomplete': 'username',
        }

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class SignUpForm(forms.ModelForm):
    error_messages = {
        'password_mismatch':  ('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Re-enter Password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

class PostForm(forms.ModelForm):


    class Meta:
        model = Post
        fields = ('title', 'description', 'address', 'start_date', 'end_date', 'start_time', 'end_time')
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
            'start_time': TimeInput(),
            'end_time': TimeInput()
        }
    title = forms.TextInput(attrs={'id': 'title',  'class':'field1', 'placeholder':'Enter event name...'})
    description = forms.TextInput(attrs={'id': 'description',  'class':'field2'})