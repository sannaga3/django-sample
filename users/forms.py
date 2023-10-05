from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from users.models import Profile, User

User = get_user_model() 

class RegisterForm(forms.ModelForm):
  username = forms.CharField(label='Username')
  email = forms.EmailField(label='Email')
  password = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput())
  password_confirm = forms.CharField(max_length=20, label="Password_confirm", widget=forms.PasswordInput())
  
  class Meta:
    model = User
    fields = ('username', 'email', 'password')
    
  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data['password']
    password_confirm = cleaned_data['password_confirm']
    if password != password_confirm:
      raise forms.ValidationError('Passwords do not match')
    
  def save(self, commit=False):
    user = super().save(commit=False)
    validate_password(self.cleaned_data.get('password'), user)
    user.set_password(self.cleaned_data.get('password'))
    user.save()
    return user
    

class ProfileForm(forms.ModelForm):
  picture = forms.FileField(label='picture')
  
  class Meta:
    model = Profile
    fields = ('picture',)
      
      
class LoginForm(forms.Form):
  email = forms.EmailField(label='Email')
  password = forms.CharField(label='Password', widget=forms.PasswordInput())


class UpdateUserForm(forms.ModelForm):
  username = forms.CharField(label='Username')
  email = forms.EmailField(label='Email')
  age = forms.IntegerField(required=False, label='Age', min_value=0)
  
  class Meta:
    model = User
    fields = ('username', 'email', 'age')
    
class UpdatePasswordForm(forms.ModelForm):
  password = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput())
  password_confirm = forms.CharField(max_length=20, label="Password_confirm", widget=forms.PasswordInput())
  
  class Meta:
    model = User
    fields = ('password',)
    
  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data['password']
    password_confirm = cleaned_data['password_confirm']
    if password != password_confirm:
      raise forms.ValidationError('Passwords do not match')
    
  def save(self, commit=False):
    user = super().save(commit=False)
    validate_password(self.cleaned_data.get('password'), user)
    user.set_password(self.cleaned_data.get('password'))
    user.save()
    return user