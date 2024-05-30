from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from iceburgcrm.models.user import User as OratorUser

def authenticated_user_required(view_func):
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('_auth_user_id')
        if user_id:
            user = OratorUser.with_('role').find(user_id)
            if user: 
                request.oratoruser = user
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('auth_app:login')) 
        else:
            return HttpResponseRedirect(reverse('auth_app:login'))  
    return wrapper



