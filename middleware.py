from django.conf import settings
import os
from iceburgcrm.models import User, Setting, ModuleGroup, Module
from inertia import share

def shared_data_middleware(get_response):
    def middleware(request):
        user = getattr(request, 'user', None)
        openai_enabled = bool(os.environ.get('OPENAI_API_KEY'))
        meetings_enabled=bool(Module.where('name', 'meetings').first())

        system_settings = Setting.get_settings(request)
        modules = ModuleGroup.with_('modules').get()

        share(request, 
              auth={
                  'user': user.to_dict() if user and user.is_authenticated else None,  
                  'openai': openai_enabled,
                  'meetings': meetings_enabled,
                  'system_settings': system_settings,
                  'modules': [{'id': m.id, 'name': m.name, 'modules': [{'id': mod.id, 'name': mod.name} for mod in m.modules.all()]} for m in modules]
              },
              ziggy='')

        return get_response(request)
    return middleware


