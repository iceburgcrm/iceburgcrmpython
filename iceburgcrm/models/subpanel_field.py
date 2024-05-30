from orator.orm import belongs_to, has_one
from auth_app.orator_config import db
import json
from iceburgcrm.models.base import BaseModel

class SubpanelField(BaseModel):
    __table__ = 'ice_subpanel_fields'

    @has_one('id', 'field_id')
    def field(self):
        from .field import Field
        return Field