from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

from .forms import (LoginForm, ProfileForm, RegisterForm, UpdatePasswordForm,
                    UpdateUserForm)
from .models import Profile


def register(request):
  form = RegisterForm(request.POST or None)
  if form.is_valid():
    try:
      user = form.save()
      return render(request, 'users/home.html', context={'user': user})  
    except ValidationError as e:
      form.add_error('password', e )
  
  return render(request, 'users/register.html', context={'form': form})

def user_login(request):
  form = LoginForm(request.POST or None)
  if form.is_valid():
    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password')
    user = authenticate(email = email, password = password)
    if user:
      if user.is_active:
        login(request, user)
        messages.success(request, 'success login')
        return redirect('users:home')
      else:
        messages.warning(request, 'user is not activated')
    else:
        messages.warning(request, 'user is not found')
  return render(request, 'users/login.html', context={'form': form})


@login_required
def user_logout(request):
  logout(request)
  messages.success(request, 'success logout')
  return redirect('users:home')
  
@login_required
def user_update(request):
  user_form = UpdateUserForm(request.POST or None, instance=request.user)
  try:
      profile = request.user.profile
  except Profile.DoesNotExist:
      profile = Profile(user=request.user)
  profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile or None)
  
  if user_form.is_valid() and profile_form.is_valid():
    user_form.save()
    profile_form.save()
    messages.success(request, 'success updated user')
    return redirect('users:home')
  elif request.POST:
    messages.warning(request, 'failed updated user')
  
  return render(request, 'users/update.html', context={'user_form': user_form, 'profile_form': profile_form, 'profile': profile})

@login_required
def password_update(request):
  form = UpdatePasswordForm(request.POST or None, instance=request.user)
  if form.is_valid():
    try:
      form.save()
      messages.success(request, 'success updated password')
      update_session_auth_hash(request, request.user)
    except ValidationError as e:
      form.add_error('password', e)
  return render(request, 'users/password_update.html', context={'form': form})

def home(request):
  return render(request, 'users/home.html')
