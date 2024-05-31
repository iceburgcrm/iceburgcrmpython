from orator import Model
from orator.orm import has_many, belongs_to, has_one
from iceburgcrm.models.base import BaseModel
from .role import Role

class User(BaseModel):
    __table__ = 'ice_users'
    __fillable__ = ['name', 'email', 'profile_pic', 'role_id', 'password']
    __hidden__ = ['password', 'remember_token']
    __casts__ = {
        'email_verified_at': 'datetime'
    }

    @has_one('id', 'role_id')
    def role(self):
        return Role
    
    @staticmethod
    def current(request):
        user_id = request.session.get('_auth_user_id')
        if user_id:
            return User.find(user_id).with_('role').first()
