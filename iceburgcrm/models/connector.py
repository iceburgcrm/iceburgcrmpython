from orator.orm import has_one, has_many
from iceburgcrm.models.endpoint import Endpoint
from iceburgcrm.models.module import Module
from iceburgcrm.models.base import BaseModel

class Connector(BaseModel):
    __table__ = 'ice_connectors'
    __casts__ = {
        'status': 'bool'
    }

    @has_many('id', 'module_id')
    def module(self):
        return Module

    @has_many('connector_id', 'id')
    def endpoints(self):
        return Endpoint