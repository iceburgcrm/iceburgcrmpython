from functools import partial
from orator import Model, DatabaseManager
from orator.orm import has_many, has_one, belongs_to
from datetime import datetime
from datetime import datetime
import faker
import json
from django.contrib.auth.hashers import make_password
from auth_app.orator_config import db
from iceburgcrm.models.field_seeder import FieldSeeder
from iceburgcrm.models.search import Search
from iceburgcrm.models.validation import Validation
from orator import Schema
import logging

class Module(Model):
    __table__ = 'ice_modules'
    
    @belongs_to
    def module_group(self):
        from .module_group import ModuleGroup
        return ModuleGroup, 'module_group_id' 


    @has_many('module_id', 'id')
    def fields(self):
        from .field import Field
        return Field.where('status', 1)

    @has_one('primary_module_id', 'id')
    def converted_modules(self):
        from .module_convertable import ModuleConvertable
        return ModuleConvertable

    @has_many
    def subpanels(self):
        from .module_subpanel import ModuleSubpanel
        return ModuleSubpanel

    @staticmethod
    def get_id(name):
        return Module.where('name', 'like', name.lower()).pluck('id').first()

    @staticmethod
    def menu():
        return Module.where('status', 1).get()

    @classmethod
    def generate(cls, seed=0, module_id=0):
        modules = Module.where('status', 1).where('create_table', 1).get()
        for module in modules:
            if module_id == 0 or (int(module_id) > 0 and module_id == module.id):
                logging.info(f'Generating module: {module.name}')
                
                db.statement(f"DROP TABLE IF EXISTS `{module.name}`")
                
                create_table_query = f"""
                CREATE TABLE `{module.name}` (
                    `id` INT AUTO_INCREMENT PRIMARY KEY,
                    `ice_slug` VARCHAR(64) UNIQUE,
                    `soft_delete` INT DEFAULT 0,
                    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                """
                
                fields = module.fields().get()
                for field in fields:
                    data_type = field.data_type.upper()
                    if data_type == 'STRING':
                        data_type = 'VARCHAR(255)'
                    elif data_type == 'TEXT':
                        data_type = 'TEXT'
                    elif data_type == 'INTEGER':
                        data_type = 'INT'
                    elif data_type == 'FLOAT':
                        data_type = 'FLOAT'
                    elif data_type == 'MEDIUMTEXT':
                        data_type = 'MEDIUMTEXT'
 
                    print ("fields", fields.serialize())
                    print ("field.data_type.upper", field.data_type.upper())
                    print ("data_type", data_type)
                    column_definition = f"`{field.name}` {data_type}"
                    print (column_definition)
                    
                    if hasattr(field, 'length') and field.length:
                        column_definition += f"({field.length})"
                    if hasattr(field, 'decimal_places') and field.decimal_places:
                        column_definition += f"(8, {field.decimal_places})"
                    
                    if field.input_type == 'checkbox':
                        field.is_nullable = False
                        field.default_value = 0
                    if field.is_nullable:
                        column_definition += " NULL"
                    elif field.default_value:
                        column_definition += f" DEFAULT {field.default_value}"
                    
                    create_table_query += f", {column_definition}"
                
                create_table_query += ") ENGINE=InnoDB"
                db.statement(create_table_query)
               
                if seed > 0 and module.faker_seed == 1:
                    field_seeder = FieldSeeder(module)
                    field_seeder.seed(seed)

        return True

    @staticmethod
    def replace_values_for_related_ids(module_id, data, start_at=0, fields=None):
        if fields is None:
            from iceburgcrm.models.field import Field
            fields = Field.where('module_id', module_id).get()

        related_modules = {}
        for field in fields:
            if field.input_type == 'related':
                related_modules[field.name] = Module.get_related_module_list(
                    field.related_module_id, field.related_field_id, field.related_value_id)

        data = data.serialize()  #
        return_data = []

        for index, items in enumerate(data):
            if index >= start_at:
                modified_item = items.copy() 
                for key, value in items.items():
                    if key in related_modules:
                        related_dict = next((rm for rm in related_modules[key] if rm['name'] == value), None)
                        if related_dict:
                            modified_item[key] = related_dict['id'] 
                return_data.append(modified_item)

        return return_data

    @staticmethod
    def replace_related_ids(module_id, data, fields=None):
        if fields is None:
            from iceburgcrm.models.field import Field
            fields = Field.where('module_id', module_id).where('input_type', 'related').get()

        related_modules = {}
        for field in fields:
           related_modules[field.name] = Module.get_related_module_list(
                field.related_module_id, field.related_field_id, field.related_value_id)

    
        data = data.serialize()
        for items in data: 
            for key, value in items.items():
                if key in related_modules and Module.value_exists_in_related_modules(related_modules, key, value):
                    for field in fields:
                        if field.name == key:
                            related_dict = Module.find_dict_by_id(related_modules[key], value)
                            if related_dict and field.related_value_id in related_dict:
                                new_value = related_dict[field.related_value_id]
                                for item2 in data:
                                   if item2.get(key):
                                        item2[key] = new_value

        return data
    
    def find_dict_by_id(dicts, id_value):
        """ Helper function to find a dictionary in a list by 'id' """
        for d in dicts:
            if d.get('id') == id_value:
                return d
        return None
    
    def value_exists_in_related_modules(related_modules, key, value):
        return any(d.get('id') == value for d in related_modules[key])
    
    def get_related_value(collection, value, attribute_name, related_value_id):
        for item in collection:
            if getattr(item, attribute_name, None) == value:
                return getattr(item, related_value_id, None)
        return None

    def get_records(module_id=None, ids=[], export=False):
        from iceburgcrm.models.settings import Setting
        from iceburgcrm.models.field import Field

        module = Module.find(module_id)
        if not module:
            raise ValueError("Module not found")

        field_names = []
        fields = Field.where('module_id', module.id).where('status', 1).get()

        for field in fields:
            field_names.append(f"{module.name}.{field.name}")
 
        query = db.table(module.name).select_raw(', '.join(field_names))

        if ids:
            query = query.where_in('id', ids)
 
        max_records = 1000
        data = query.take(max_records).get()
        
        if export:
            data = Module.replace_related_ids(module_id, data)
        
        return data
    
    @staticmethod
    def get_record(module_id=None, record_id=None, replace_related_ids=False):
        module = Module.find(module_id)
        if not module:
            return None 
        
   
        results = db.table(module.name).select_raw(
            f"{module.name}.*, {module.name}.{module.primary_field} as {module.name}_row_id, "
            f"{module.name}.{module.primary_field} as row_id"
        ).where(module.primary_field, record_id).first()
     
        if replace_related_ids and results:
            results = Search.replace_related_ids(module_id, results)

        return results
    
    @staticmethod
    def get_previous_next(module_id, record_id):
        previous = 0
        next_id = 0  

        module = Module.find(module_id)
        if module:
            previous = db.table(module.name) \
                        .where(module.primary_field, '<', record_id) \
                        .order_by(module.primary_field, 'desc') \
                        .first()
            next_id = db.table(module.name) \
                       .where(module.primary_field, '>', record_id) \
                       .order_by(module.primary_field, 'asc') \
                       .first()

            previous = previous[module.primary_field] if previous else 0
            next_id = next_id[module.primary_field] if next_id else 0

        return [previous, next_id]
    
    def save_record(module_id, request, return_id=False):
        from .field import Field
        from .relationship import Relationship
        from .work_flow_data import WorkFlowData
        validator = Validation()

        fake = faker.Faker()
        data = {}
        rules = {}
        relationship = None

        record_id = request.get('record_id', 0)
        relationship_id = request.get('relationship_id', 0)
        if relationship_id and int(relationship_id) > 0:
            relationship = Relationship.find(relationship_id)

        for key, value in request.items():
            pieces = key.split('__')
            if len(pieces) > 1:
                field = Field.where('module_id', pieces[0]).where('name', pieces[1]).first()
                if field:
                    if field.input_type == 'password':
                        value = make_password(value)
                    elif field.input_type == 'date':
                        value = datetime.strptime(value, "%Y-%m-%d")
                    elif field.input_type == 'checkbox':
                        value = bool(value)
                    data.setdefault(pieces[0], {})[field.name] = value

                    if field.validation:
                        rules.setdefault(pieces[0], {})[field.name] = field.validation

        id = ''
        modules = []

        for key, values in data.items():
            
            module = Module.find(key)
            if module:
                if record_id and int(record_id) > 0:
                    if relationship_id and int(relationship_id) > 0:
                        pass
                    else:
                        values['updated_at'] = datetime.now()
                        db.table(module.name).where(module.primary_field, record_id).update(values)
                        id = record_id
                else:
                    values['created_at'] = datetime.now()
                    values['updated_at'] = datetime.now()
                    values['ice_slug'] = fake.bothify(text='???????????????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')

                    id = db.table(module.name).insert_get_id(values)
                    WorkFlowData.insert({
                        'from_id': request.get('from_id', 0),
                        'from_module_id': request.get('from_module', 0),
                        'to_id': id,
                        'to_module_id': module.id,
                        'created_at': datetime.now(),
                        'updated_at': datetime.now(),
                    })

                modules.append(key)

        return id
    
    def get_related_module_list(module_id, related_field_id, related_value_id):
        module = Module.find_or_fail(module_id) 

        results = db.table(module.name).select(related_field_id, related_value_id).get().serialize()

        return results
    
    def get_id(module_name):
        module=Module.where('name', module_name).first()
        return module.id
    
    def delete_records(module_id, data):
        
        module = Module.find(module_id)
        
        if not module:
            raise ValueError("Module not found")

        if isinstance(data, dict):
            data = [data['record_id']]
        elif isinstance(data, list):
            if all(isinstance(item, dict) for item in data):
                try:
                    data = [item['record_id'] for item in data]
                except KeyError:
                    raise ValueError("Each dictionary in the data list must contain the 'record_id' key")
            elif all(isinstance(item, int) for item in data):
                pass
            else:
                raise ValueError("Data must be a list of dictionaries with 'record_id' or a list of integers")
        elif isinstance(data, int):
            data = [data]
        else:
            raise ValueError("Data must be a dictionary with 'record_id', a list of such dictionaries, a list of integers, or a single integer")
        
        deleted_count = db.table(module.name).where_in(module.primary_field, data).delete()
        
        return deleted_count

