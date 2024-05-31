from orator.orm import belongs_to, has_one
from auth_app.orator_config import db
import json
from iceburgcrm.models.base import BaseModel

class ModuleConvertable(BaseModel):
    __table__ = 'ice_module_convertables'

    @has_one('id', 'module_id')
    def module(self):
        from .module import Module
        return Module

    @has_one('id', 'primary_module_id')
    def primary_module(self):
        from .module import Module
        return Module