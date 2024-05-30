import json
from django.http import HttpResponseNotFound
from orator.orm import has_many, belongs_to
from iceburgcrm.models.relationship import Relationship
from iceburgcrm.models.field import Field
from iceburgcrm.models.settings import Setting
from iceburgcrm.models.search import Search
from auth_app.orator_config import db
from iceburgcrm.models.base import BaseModel

class ModuleSubpanel(BaseModel):
    __table__ = 'ice_module_subpanels'

    @belongs_to
    def module(self):
        from .module import Module
        return Module

    @belongs_to
    def relationship(self):
        return Relationship
    
    @has_many('subpanel_id', 'id')
    def subpanel_fields(self):
        from .subpanel_field import SubpanelField
        return SubpanelField


    @classmethod
    def get_subpanels(cls, module_id, id):
        from .module import Module
        subpanels = cls.where('module_id', module_id).with_('relationship').with_('module').get()
        return_array = []
        for subpanel in subpanels:
            data = []
            modules = subpanel.relationship.modules.split(',')
            subpanel_module = Module.find(subpanel.module_id).first()
            if modules:
                relationship_query = db.table(subpanel.relationship.name)
                table_primary_ids = ''
                for module_id in modules:
                    join_module = Module.where('id', module_id).first()
                    relationship_query.join(join_module.name, f"{subpanel.relationship.name}.{join_module.name}_id", '=', f"{join_module.name}.id")
                    table_primary_ids += f", {join_module.name}.id as {join_module.name}_row_id"
                data = relationship_query.select_raw(f"{subpanel.subpanel_fields}, {subpanel.relationship.name}.id as row_id{table_primary_ids}")\
                                         .where(f"{subpanel_module.name}_id", id)\
                                         .order_by(f"{subpanel.relationship.name}.{subpanel.list_order_column}", subpanel.list_order)\
                                         .take(subpanel.list_size)\
                                         .get()

            subpanel_fields = []
            for fields in subpanel.subpanel_fields.split(','):
                field_parts = fields.split(' as ')
                if len(field_parts) > 1:
                    field = field_parts[1].split('__')
                    module = Module.where('name', field[0].capitalize()).first()
                    if module:
                        subpanel_fields.append(Field.where('name', field[1]).where('module_id', module.id).with_('module').with_('related_module').first())

            field_names = [field_part.split(' as ')[1] for field_part in subpanel.subpanel_fields.split(',') if ' as ' in field_part]
            return_array.append({
                'id': subpanel.id,
                'name': subpanel.name,
                'label': subpanel.label,
                'field_labels': field_names,
                'fields': subpanel_fields,
                'data': data,
            })

        return return_array
    
    def get_subpanel_data(request, subpanel_id, params):
        subpanel = ModuleSubpanel.where('id', subpanel_id).with_('subpanel_fields.field.module').first()
        if not subpanel:
            return HttpResponseNotFound("Subpanel not found")

        # Serialize the subpanel data
        subpanel_data = subpanel.to_dict()

        # Handle additional data processing
        default_per_page = int(Setting.get_setting('submodule_search_per_page'))
        options = {
            'relationship_id': subpanel.relationship_id,
            'search_type': 'relationship',
            'per_page': default_per_page,
            'search_field': params.get('search_field'),
            'search_text': params.get('search_text') if len(params.get('search_text', '')) > 2 else None
        }

        if (params['search_field']) and params['search_text'] and len(params['search_text']) > 2:
            options[params['search_field']] = params['search_text']
        

        search_data = Search.get_data(request, options)
        subpanel_data.update({
            'fields': [field.to_dict() for field in subpanel.subpanel_fields],
            'data': search_data
        })
     

        return subpanel_data

    @staticmethod
    def process_records(subpanel_id, selected_records, new_records, record_id=0):
        from .module import Module
        subpanel = ModuleSubpanel.where('id', subpanel_id).with_('relationship.relationship_module.module.fields.module').first()

        for relationship_module in subpanel.relationship.relationship_module:
            if relationship_module.module.id and new_records.get(str(relationship_module.module.id)):
                new_record = new_records[str(relationship_module.module.id)]
                new_record.update({
                    'from_id': new_records['from_id'],
                    'from_module': new_records['from_module']
                })

                selected_records[str(relationship_module.module.id)] = Module.save_record(relationship_module.module.id, new_record)


        return Relationship.save_record(subpanel.relationship_id, selected_records, record_id)
    
    @staticmethod
    def select_field_to_database_field(fields):
        from .module import Module
        fields_array = []
        fields_data = fields.split(',')

        for field in fields_data:
            parts = field.split('.')
            module = Module.where('name', parts[0].lower().capitalize()).first()
            if module:
                item = Field.where('name', parts[1]).where('module_id', module.id).with_('module', 'related_module').first()
                if item:
                    fields_array.append(item.serialize())

        return fields_array
    
    @staticmethod
    def parse_request(request):
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.GET.dict()

        selected_records = {}
        new_records = {}
        subpanel_id = 0
        record_id = 0

        for key, value in data.items():
            if '__' in key:
                parts = key.split('__')
                new_records.setdefault(parts[0], {})[key] = value
            elif 'module_records' == key:
                selected_records = value if isinstance(value, dict) else {}
            elif 'subpanel_id' == key:
                subpanel_id = int(value)  
            elif 'record_id' == key:
                record_id = int(value)  

        return subpanel_id, selected_records, new_records, record_id

    def to_dict(self):
        """
        Convert the ModuleSubpanel instance to a dictionary, including nested relationships.
        """
        module = self.module.serialize() if self.module else None
        relationship = self.relationship.serialize() if self.relationship else None
        subpanel_fields = [field.serialize() for field in self.subpanel_fields] if self.subpanel_fields else []

        return {
            'id': self.id,
            'name': self.name,
            'module': module,
            'relationship': relationship,
            'subpanel_fields': subpanel_fields
        }


