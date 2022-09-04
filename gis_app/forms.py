from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Profile
from django.contrib.gis import forms as gform

User = get_user_model()

class SignInForm(forms.ModelForm):
    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(SignInForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control col-12'
            self.fields['username'].widget.attrs['placeholder'] = 'UserName'
            self.fields['password'].widget.attrs['placeholder'] = 'Password'

    class Meta:
        model = User
        fields = ['username', 'password'] 

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )

    def get_user(self):
        return self.user_cache




class SignUpForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control col-12'
            self.fields['username'].widget.attrs['placeholder'] = 'UserName'
            self.fields['password'].widget.attrs['placeholder'] = 'Password'
            self.fields['first_name'].widget.attrs['placeholder'] = 'First name'
            self.fields['last_name'].widget.attrs['placeholder'] = 'Last name'

            
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']


