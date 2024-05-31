from orator import Model
from orator.orm import has_many
from .module import Module

class ModuleGroup(Model):
    __table__ = 'ice_module_groups'


    @has_many('module_group_id', 'id')
    def modules(self):
        return Module
    
    @property
    def review_avg(self):
        modules = self.modules().where('status', 1).get()
        total = sum(module.review_avg for module in modules) if modules else 0
        return total / len(modules) if modules else 0
