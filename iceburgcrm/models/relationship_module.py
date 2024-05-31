from orator import Model
from orator.orm import belongs_to

class RelationshipModule(Model):
    __table__ = 'ice_relationship_modules'
    __guarded__ = []

    @belongs_to('relationship_id', 'id')
    def relationship(self):
        from .relationship import Relationship
        return Relationship

    @belongs_to('module_id', 'id')
    def module(self):
        from .module import Module
        return Module

    @belongs_to('module_id', 'id')
    def module_fields(self):
        from .module import Module
        return Module.with_('fields')
