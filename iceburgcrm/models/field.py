from orator.orm import belongs_to, has_one
from auth_app.orator_config import db
import json
from iceburgcrm.models.base import BaseModel

class Field(BaseModel):
    __table__ = 'ice_fields'
    __guarded__ = ['id']

    @belongs_to('module_id', 'id')
    def module(self):
        from .module import Module
        return Module

    @has_one('id', 'related_module_id')
    def related_module(self):
        from .module import Module
        return Module

    def generate(self):
        from .field import Field
        fields = self.where('status', 1).get()
        for field in fields:
            self.generate_table(field)
        print('generateTable done')

    @staticmethod
    def generate_table(module):
        data = json.loads(module.data) 
        for item in data:
            db.table(module.name).insert(dict(item))
        print(f'generate {module.name} Data')

    @staticmethod
    def get_field(data, order=0):
        default_data = {
            'name': '',  
            'label': '', 
            'module_id': 0, 
            'validation': '', 
            'input_type': 'text',  
            'data_type': 'string',  
            'field_length': 245,  
            'required': False,  
            'is_nullable': True,  
            'default_value': '',
            'read_only': False, 
            'related_module_id': 0, 
            'related_field_id': 0, 
            'related_value_id': 0, 
            'decimal_places': None, 
            'status': 1, 
            'search_display': 1, 
            'list_display': 1, 
            'edit_display': 1,  
            'view_display': 1, 
            'display_order': 9999,  
            'search_order': 9999,  
            'list_order': 9999,  
            'edit_order': 9999,  
        }

        default_data.update(data)
        return default_data

    @staticmethod
    def get_select_fields(join_module):
        select_fields = []
        fields = Field.where('module_id', join_module.id).with_('module').with_('related_module').get()
        for field in fields:
            select_fields.append(f'{join_module.name}.{field.name} as {join_module.name}__{field.name}')
        return select_fields

    @staticmethod
    def get_related_field_data(module_id):
        from .module import Module
        output = {}
        fields = Field.where('module_id', module_id).where('related_module_id', '>', 0).where('status', 1).get()
        for field in fields:

            related_module = Module.find(field.related_module_id)
            output[field.name] = db.table(related_module.name).get().serialize()
        
        return output
