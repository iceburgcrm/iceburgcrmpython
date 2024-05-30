from django.contrib import messages
from inertia.share import share
from iceburgcrm.models import User, Setting, ModuleGroup, Module
from django.conf import settings
import os


def inertia_share(get_response):
  def middleware(request):
    
    user=None
    user_id = request.session.get('_auth_user_id')
    if user_id:
        user = User.find(user_id).with_('role').first().serialize()
        
    openai_enabled = bool(os.environ.get('OPENAI_API_KEY'))
    meetings_enabled=bool(Module.where('name', 'meetings').first())
    

    system_settings = Setting.get_settings(request)
    theme = system_settings.get('theme', 'default')  # Default to 'default' theme if not set

    modules = ModuleGroup.with_('modules').get().serialize()

    share(request, 
            auth={
                'user': user,  
                'openai': openai_enabled,
                'meetings': meetings_enabled,
                'system_settings': system_settings,
                'modules': modules,
            },theme=theme)

    return get_response(request)
  return middleware