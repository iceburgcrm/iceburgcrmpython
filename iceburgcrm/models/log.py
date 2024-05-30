from orator.orm import has_one
from iceburgcrm.models.module import Module
from iceburgcrm.models.user import User
from iceburgcrm.models.base import BaseModel

class Log(BaseModel):
    __table__ = 'ice_logs'

    @has_one('module_id')  
    def module(self):
        return Module

    @has_one('id', 'user_id')
    def user(self): 
        return User
