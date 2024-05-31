# backends.py
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.shortcuts import redirect
from iceburgcrm.models.user import User as OratorUser
from orator.exceptions.orm import ModelNotFound
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.utils.crypto import salted_hmac, get_random_string
import bcrypt

class OratorBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = OratorUser.where('email', username).first()
            if user and self.check_password(password, user.password):
                return user
        except ModelNotFound:
            pass
        return None
    
    def get_or_create_django_user(self, orator_user):
        try:
            user, created = User.objects.get_or_create(username=orator_user.email)
        except User.DoesNotExist:
            user = User(username=orator_user.email, email=orator_user.email)
            user.is_active = True
            user.set_unusable_password()
            user.save()
        else:
            if created:
                user.email = orator_user.email
                user.is_active = True
                user.set_unusable_password()
                user.save()
        return user

    def check_password(self, raw_password, hashed_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))
    

    def authenticated_user_required(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.session.get('is_authenticated'):
                return redirect('auth_app:login')  
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    
    def custom_logout(request):
        request.session.flush() 
        return redirect('login_url')
    
    def custom_login(self, request, orator_user):
        user_id = orator_user.id  

        session_auth_hash = salted_hmac(
            "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash",
            orator_user.password 
        ).hexdigest()

        if SESSION_KEY in request.session:
            if request.session[SESSION_KEY] != user_id:
                request.session.flush()
        else:
            request.session.cycle_key()

        backend_path = 'auth_app.backends.OratorAuthenticationBackend'

        request.session[SESSION_KEY] = user_id
        request.session[BACKEND_SESSION_KEY] = backend_path
        request.session[HASH_SESSION_KEY] = session_auth_hash

        request.session.set_expiry(0) 

        request.session['user_data'] = {
            'email': orator_user.email, 
            'name': orator_user.name 
        }


    def get_user(self, user_id):
        print("Getting user for ID:", user_id)
        try:
            user = OratorUser.query.get(user_id)
            print("User found:", user)
            return user
        except OratorUser.DoesNotExist:
            print("No user found for ID:", user_id)
            return None
