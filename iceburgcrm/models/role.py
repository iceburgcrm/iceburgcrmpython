from orator import Model
from orator.orm import belongs_to, has_many

class Role(Model):
    __table__ = 'ice_roles'

    @belongs_to('module_id', 'id')
    def module(self):
        from .module import Module
        return Module

    @has_many('role_id', 'id')
    def permissions(self):
        from .permission import Permission
        return Permission
