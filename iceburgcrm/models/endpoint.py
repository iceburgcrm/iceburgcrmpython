from orator.orm import has_one
from iceburgcrm.models.module import Module
from auth_app.orator_config import db
from django.utils import timezone
from iceburgcrm.models.base import BaseModel

class Endpoint(BaseModel):
    __table__ = 'ice_endpoints'  
    __casts__ = {
        'status': 'bool'  
    }
