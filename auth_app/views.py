import json
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import (
    PasswordChangeForm, PasswordResetForm, SetPasswordForm
)
from django.shortcuts import redirect
from django.urls import reverse, get_resolver
from django.http import JsonResponse
from django.middleware.csrf import get_token
from inertia import render
from auth_app.backends import OratorBackend
from iceburgcrm.models.user import User as OratorUser


def login_request(request):
    context = {
        'loginUrl': reverse('auth_app:login'),
        'csrfToken': get_token(request) 
    }
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8')) 
        email = data.get('email')
        password = data.get('password')
        backend = OratorBackend()
        request.session.flush()
        user = authenticate(request, username=email, password=password)
        if user:
            backend.custom_login(request, user)
            return JsonResponse({
                'login': True,
            })
        else:
            return JsonResponse({
                'login': False,
                'error': 'Invalid credentials'
            })
    else: 
        return render(request, 'Auth/Login', context)


def logout_request(request):
    logout(request)
    return redirect('auth_app:login')

def password_change_request(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('password_change_done')
        else:
            return render(request, 'Auth/PasswordChange', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Auth/PasswordChange', {'form': form})

def password_change_done_request(request):
    return render(request, 'Auth/PasswordChangeDone')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request=request)
            return redirect('password_reset_done')
        else:
            return render(request, 'Auth/PasswordReset', {'form': form})
    else:
        form = PasswordResetForm()
    return render(request, 'Auth/PasswordReset', {'form': form})

def password_reset_done_request(request):
    return render(request, 'Auth/PasswordResetDone')

def password_reset_confirm_request(request, uidb64, token):
    return render(request, 'Auth/PasswordResetConfirm')

def password_reset_complete_request(request):
    return render(request, 'Auth/PasswordResetComplete')

def js_routes(request):
    """
    Returns a JSON object with all named Django URL patterns.
    """
    resolver = get_resolver()
    routes = {}
    for url_pattern in resolver.url_patterns:
        if url_pattern.name:
            # Building a pattern without domain and arguments for simplicity
            pattern = str(url_pattern.pattern)
            routes[url_pattern.name] = pattern.replace('^', '').replace('$', '')
    return JsonResponse(routes)

def welcome(request):
    pass


