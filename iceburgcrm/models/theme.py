from orator.orm import belongs_to, has_one
from auth_app.orator_config import db
import json
from iceburgcrm.models.base import BaseModel


class Theme(BaseModel):
    __table__ = 'ice_themes'