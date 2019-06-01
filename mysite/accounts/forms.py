from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ModelForm
from .models import Product, Todo, UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    #password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password'
        )

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['description', 'city', 'phone', 'ingredients']

class CustomAuthentificationForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            print('inactive')
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = ['name_product', 'description', 'price']


class TodoForm(forms.Form):

    class Meta:
        model = Todo
        fields = ['text']

    text = forms.CharField(max_length=40, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder' : 'Enter todo e.g. Delete junk files', 'aria-label':'Todo', 'aria-describedby': 'add-btn'}
    ))


