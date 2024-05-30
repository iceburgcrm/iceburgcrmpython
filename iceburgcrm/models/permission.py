from orator import Model
from orator.orm import has_one
from datetime import datetime
from iceburgcrm.models.user import User
from auth_app.orator_config import db

class Permission(Model):
    __table__ = 'ice_permissions'
    types = ['read', 'write', 'import', 'export']

    @has_one('id', 'module_id')
    def modules(self):
        from .module import Module
        return Module.where('status', 1)

    @has_one('id', 'role_id')
    def roles(self):
        from .role import Role
        return Role

    @staticmethod
    def check_permission(module_id=0, current_user=None, type='read', message=''):
        from iceburgcrm.models.module import Module
        if type not in Permission.types:
            return False
        current_module=Module.where('id', module_id).first()

        if current_user.role.id != 1 and current_module.admin:
            return False

        from iceburgcrm.models.log import Log   
        Log.insert({
            'user_id': current_user.id,
            'type': type,
            'message': message,
            'module_id': module_id,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        })
        permission=Permission.where('module_id', module_id)\
                         .where('role_id', current_user.role_id)\
                         .where(f'can_{type}', 1).first()
        if permission:
            return permission.id
        
        return None

    @staticmethod
    def get_permissions(module_id, user):
        permissions = {}
        for type in Permission.types:
            permissions[type] = int(bool(Permission.check_permission(module_id, user, type)))
        
        return permissions
