from datetime import datetime
from auth_app.orator_config import db
from orator import Schema
from orator.seeds import Seeder
from iceburgcrm.models.field import Field
from iceburgcrm.models.module import Module
from iceburgcrm.models.module_group import ModuleGroup
from iceburgcrm.models.module_convertable import ModuleConvertable
import logging
from django.utils.crypto import get_random_string
from faker import Faker

class CoreSeeder():
     
    @staticmethod   
    def migration():
        schema = Schema(db)

        schema.drop_if_exists('ice_users')

        with schema.create('ice_users') as table:
            table.increments('id')
            table.string('name')
            table.string('email').unique()
            table.timestamp('email_verified_at').nullable()
            table.string('password')
            table.text('profile_pic').nullable()
            table.integer('role_id').default(2)
            table.string('ice_slug').default('')
            table.string('remember_token').nullable()
            table.timestamps()

        schema.drop_if_exists('ice_fields')
        schema.drop_if_exists('ice_modules')
        schema.drop_if_exists('ice_module_groups')

        # Create the 'ice_modules' table
        with schema.create('ice_modules') as table:
            table.increments('id')
            table.string('name', 100).default('')
            table.string('label').default('')
            table.string('description', 245).default('')
            table.integer('status').default(1)
            table.integer('faker_seed').default(1)
            table.integer('create_table').default(1)
            table.integer('view_order').default(0)
            table.integer('admin').default(0)
            table.integer('parent_id').default(0)
            table.integer('primary').default(0)
            table.string('primary_field', 64).default('id')
            table.string('icon', 128).default('CircleStackIcon')
            table.integer('module_group_id')
            table.timestamps()

        # Create the 'ice_fields' table
        with schema.create('ice_fields') as table:
            table.increments('id')
            table.string('name', 245)
            table.string('label', 245)
            table.integer('module_id')
            table.string('validation', 245).nullable()
            table.string('input_type', 245).default('text')
            table.string('data_type', 100)
            table.integer('field_length').nullable()
            table.integer('required').default(0)
            table.tiny_integer('is_nullable').default(0)
            table.string('default_value', 245).default('')
            table.tiny_integer('read_only').default(0)
            table.integer('related_module_id').default(0)
            table.string('related_field_id').default('')
            table.string('related_value_id').default('')
            table.integer('decimal_places').nullable()
            table.tiny_integer('status').default(1)
            table.tiny_integer('search_display').default(1)
            table.tiny_integer('list_display').default(1)
            table.tiny_integer('edit_display').default(1)
            table.tiny_integer('view_display').default(1)
            table.integer('display_order').default(9999)
            table.integer('search_order').default(9999)
            table.integer('list_order').default(9999)
            table.integer('edit_order').default(9999)
            table.timestamps()
            table.index('module_id')

        # Create the 'ice_module_groups' table
        with schema.create('ice_module_groups') as table:
            table.increments('id')
            table.string('name', 245)
            table.string('label', 245).nullable()
            table.integer('view_order').default(0)

        schema.drop_if_exists('ice_relationships')
        schema.drop_if_exists('ice_settings')
        schema.drop_if_exists('ice_module_subpanels')
        schema.drop_if_exists('ice_relationship_modules')
        schema.drop_if_exists('ice_workflow_actions')
        schema.drop_if_exists('ice_datalet_types')

        # Create the 'ice_relationships' table
        with schema.create('ice_relationships') as table:
            table.increments('id')
            table.string('name', 245)
            table.string('modules')
            table.string('related_field_types').nullable()
            table.integer('status').default(1)
            table.timestamps()

        # Create the 'ice_settings' table
        with schema.create('ice_settings') as table:
            table.increments('id')
            table.string('name')
            table.string('value').default('')
            table.text('additional_data').nullable()
            table.timestamps()

        # Create the 'ice_module_subpanels' table
        with schema.create('ice_module_subpanels') as table:
            table.increments('id')
            table.string('subpanel_filter').nullable()
            table.string('name', 245)
            table.string('label', 245)
            table.string('module_id')
            table.integer('list_size').default(10)
            table.string('list_order_column').default('id')
            table.string('list_order').default('desc')
            table.integer('relationship_id').default(0)
            table.integer('status').default(1)
            table.integer('saved_search_id').default(0)
            table.timestamps()

        # Create the 'ice_relationship_modules' table
        with schema.create('ice_relationship_modules') as table:
            table.increments('id')
            table.integer('module_id')
            table.integer('relationship_id')
            table.timestamps()

        # Create the 'ice_workflow_actions' table
        with schema.create('ice_workflow_actions') as table:
            table.increments('id')
            table.string('name')
            table.timestamps()

        # Create the 'ice_datalet_types' table
        with schema.create('ice_datalet_types') as table:
            table.increments('id')
            table.string('name').default('')
            table.timestamps()

        table_names = [
    'ice_datalets', 'ice_subpanel_fields', 'ice_module_convertables', 
    'ice_permissions', 'ice_roles', 'ice_logs', 'ice_work_flow_data', 
    'ice_themes', 'ice_connectors', 'ice_schedules', 'ice_endpoints', 
    'ice_password_resets', 'ice_failed_jobs', 'personal_access_tokens'
]
        for table_name in table_names:
            schema.drop_if_exists(table_name)

        # Create tables
        # Ice Datalets
        with schema.create('ice_datalets') as table:
            table.increments('id')
            table.string('name').default('')
            table.string('label').default('')
            table.integer('type').default(1)
            table.integer('role_id').default(0)
            table.integer('field_id').default(0)
            table.integer('module_id').default(0)
            table.integer('relationship_id').default(0)
            table.integer('size').default(6)
            table.integer('display_order').default(0)
            table.integer('active').default(1)
            table.timestamps()

        # Ice Subpanel Fields
        with schema.create('ice_subpanel_fields') as table:
            table.increments('id')
            table.integer('field_id')
            table.integer('subpanel_id')
            table.string('label').default('')
            table.timestamps()

        # Ice Module Convertables
        with schema.create('ice_module_convertables') as table:
            table.increments('id')
            table.integer('primary_module_id')
            table.integer('module_id')
            table.integer('level')
            table.timestamps()

        # Ice Permissions
        with schema.create('ice_permissions') as table:
            table.increments('id')
            table.integer('module_id').default(0)
            table.integer('role_id').default(0)
            table.integer('can_read').default(1)
            table.integer('can_write').default(1)
            table.integer('can_delete').default(1)
            table.integer('can_export').default(1)
            table.integer('can_import').default(1)
            table.timestamps()
            table.index('module_id')
            table.index('role_id')

        # Ice Roles
        with schema.create('ice_roles') as table:
            table.increments('id')
            table.string('name', 200)
            table.string('ice_slug').default('')
            table.timestamps()

        # Ice Logs
        with schema.create('ice_logs') as table:
            table.increments('id')
            table.integer('module_id').default(0)
            table.string('type', 16).default('')
            table.string('message', 200).default('')
            table.integer('user_id').default(0)
            table.timestamps()

        # Ice Work Flow Data
        with schema.create('ice_work_flow_data') as table:
            table.increments('id')
            table.integer('from_id').default(0)
            table.integer('from_module_id').default(0)
            table.integer('to_id').default(0)
            table.integer('to_module_id').default(0)
            table.timestamps()

        # Ice Themes
        with schema.create('ice_themes') as table:
            table.increments('id')
            table.string('name', 255)
            table.string('ice_slug').default('')
            table.timestamps()

        # Ice Connectors
        with schema.create('ice_connectors') as table:
            table.increments('id')
            table.string('name', 200)
            table.string('auth_key').default('')
            table.string('base_url', 200).default('')
            table.integer('status').default(1)

        # Ice Schedules
        with schema.create('ice_schedules') as table:
            table.increments('id')
            table.string('name', 200).default('')
            table.integer('start_hour')
            table.integer('start_minute').default(0)
            table.integer('start_day').default(0)
            table.enum('frequency', ['once', 'daily', 'weekly', 'monthly', 'yearly']).default('once')
            table.integer('status').default(1)
            table.timestamps()

        # Ice Endpoints
        with schema.create('ice_endpoints') as table:
            table.increments('id')
            table.integer('connector_id')
            table.string('endpoint', 190).default('')
            table.string('class_name', 100).default('default')
            table.string('request_type', 10).default('GET')
            table.string('params', 190).default('')
            table.string('headers', 190).default('')
            table.integer('status').default(1)
            table.integer('last_run_status').default(1)
            table.string('last_run_message', 190).default('')
            table.string('last_run_data', 190).default('')
            table.integer('last_ran').default(0)

        # Ice Password Resets
        with schema.create('ice_password_resets') as table:
            table.string('email').index()
            table.string('token')
            table.timestamp('created_at').nullable()

        # Ice Failed Jobs
        with schema.create('ice_failed_jobs') as table:
            table.increments('id')
            table.string('uuid').unique()
            table.text('connection')
            table.text('queue')
            table.long_text('payload')
            table.long_text('exception')
            table.timestamp('failed_at').use_current()

        # Personal Access Tokens
        with schema.create('personal_access_tokens') as table:
            table.increments('id')
            table.string('tokenable_type')
            table.integer('tokenable_id')
            table.string('name')
            table.string('token', 64).unique()
            table.text('abilities').nullable()
            table.timestamp('last_used_at').nullable()
            table.timestamps()

        db.statement('ALTER TABLE ice_settings MODIFY additional_data MEDIUMTEXT')

        print("All tables were recreated successfully!")

    @staticmethod
    def module():
        ModuleGroup.truncate()
        Module.truncate()
        ModuleConvertable.truncate()

        CoreSeeder.seed_modules()
        CoreSeeder.seed_module_groups()

    @staticmethod
    def seed_modules():
        order = 0
        modules = [
            {'name': 'ice_users', 'label': 'ICE Users', 'description': 'User management for ICE system', 'view_order': order+52, 'module_group_id': 6, 'icon': 'UserPlusIcon', 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_roles', 'label': 'ICE Roles', 'description': 'Role management for ICE system', 'view_order': order+54, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 0},
            {'name': 'ice_themes', 'label': 'ICE Themes', 'description': 'Theme settings for ICE system', 'view_order': order+55, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_module_subpanels', 'label': 'ICE Module Subpanels', 'description': 'Subpanels within the ICE framework', 'view_order': order+15, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_modules', 'label': 'ICE Modules', 'description': 'Modules within the ICE framework', 'view_order': order+16, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_fields', 'label': 'ICE Fields', 'description': 'Fields within the ICE framework', 'view_order': order+20, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_datalets', 'label': 'ICE Datalets', 'description': 'Data widgets for ICE dashboards', 'view_order': order+21, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_relationships', 'label': 'ICE Relationships', 'description': 'Manage relationships within the ICE system', 'view_order': order+24, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 1, 'create_table': 0, 'faker_seed': 0}
        ]
                
        Module.insert(modules)

    @staticmethod
    def ai_generate_seeder():
       
        seed_amount=50
        Module.generate(seed_amount)

        faker = Faker()
        modules = db.table('ice_modules').where('status', 1).where('create_table', 1).where('faker_seed', 0).get()

        for module in modules:
            method_name = module.name.lower() + "_data"
 
            if hasattr(CoreSeeder, method_name):
                method = getattr(CoreSeeder, method_name)
                if callable(method):
                    print(f"The method '{method_name}' exists and is callable.")
                else:
                    print(f"The attribute '{method_name}' exists but is not callable.")
                logging.info(f'Generating module: {module.name}')
                table_name = module.name.lower()
                db.table(table_name).truncate()
                data_method = getattr(CoreSeeder, method_name)
                data = data_method()
                if data:
                    for row in data:
                        row['ice_slug'] = get_random_string(32)  # Generates a random hex string
                        db.table(table_name).insert(row)
            else:
                print(f"The method '{method_name}' does not exist.")

        print("Generating modules and roles")
        CoreSeeder.add_modules_and_roles()

    @staticmethod
    def ai_module_seeder():

        order = 0
        modules = [
            {'name': 'states', 'label': 'States', 'description': 'Manage different states', 'view_order': order+1, 'module_group_id': 6, 'icon': 'GlobeAmericasIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 0},
            {'name': 'countries', 'label': 'Countries', 'description': 'Manage different countries', 'view_order': order+2, 'module_group_id': 6, 'icon': 'GlobeAltIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 0},
            {'name': 'currency', 'label': 'Currency', 'description': 'Currency management and settings', 'view_order': order+3, 'module_group_id': 6, 'icon': 'GlobeAltIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 0},
        ]
                
        Module.insert(modules)

    @staticmethod
    def seed_module_groups():
        module_groups = [
            {'id': 6, 'name': 'admin', 'label': 'Admin', 'view_order': 0},
        ]
        ModuleGroup.insert(module_groups)

    @staticmethod
    def field():
        Field.truncate()

        modules = Module.get()
        for module in modules:
            method_name = module.name
            if hasattr(CoreSeeder, method_name):
                logging.info(f'Task Status: Pre {method_name} Generation Started')
                getattr(CoreSeeder, method_name)(module.id)
                logging.info(f'Task Status: {method_name} Generation Completed')
            else:
                logging.info(f'Task Status: {method_name} Generation Skipped - No method')


    @staticmethod
    def generate():
        
        print("Generating users")
        CoreSeeder.add_users()
        print("Generating settings")
        CoreSeeder.add_settings()
        print("Generating connectors")
        CoreSeeder.add_connectors()
        print("Generating datalet types")
        CoreSeeder.add_datalet_types()
        print("Generating datalets")
        CoreSeeder.add_datalets()
        print("Add themes")
        CoreSeeder.add_theme()
        print("Add themes")
        CoreSeeder.add_theme()

        seed_amount=50
        Module.generate(seed_amount)


        print("Generating modules and roles")
        CoreSeeder.add_modules_and_roles()
      
    
    @staticmethod
    def add_theme():
        method_name = "ice_themes_data"
        data_method = getattr(CoreSeeder, method_name)
        data = data_method()
        if data:
            for row in data:
                row['ice_slug'] = get_random_string(32)  # Generates a random hex string
                db.table("ice_themes").insert(row)

    @staticmethod
    def states(module_id):
        fields = [
            {'name': 'code', 'label': 'Code', 'module_id': module_id, 'field_length': 4},
            {'name': 'abbreviation', 'label': 'Abbreviation', 'module_id': module_id, 'field_length': 4},
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 120}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def countries(module_id):
        fields = [
            {'name': 'code', 'label': 'Code', 'module_id': module_id, 'field_length': 16},
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 100},
            {'name': 'flag', 'label': 'Flag', 'module_id': module_id, 'input_type': 'image', 'data_type': 'MEDIUMTEXT'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def ice_themes(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 32}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def ice_modules(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'read_only': 1, 'input_type': 'text'},
            {'name': 'label', 'label': 'Label', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'boolean'},
            {'name': 'parent_id', 'label': 'Parent Module', 'module_id': module_id, 'input_type': 'related', 'related_module_id': module_id, 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'view_order', 'label': 'View Order', 'module_id': module_id, 'input_type': 'text', 'data_type': 'Integer'},
            {'name': 'admin', 'label': 'Admin Module', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'Boolean'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def ice_fields(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'read_only': 1, 'input_type': 'text'},
            {'name': 'label', 'label': 'Label', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'input_type', 'label': 'Input Type', 'module_id': module_id, 'field_length': 16, 'input_type': 'text'},
            {'name': 'validation', 'label': 'Validation', 'module_id': module_id, 'field_length': 16, 'input_type': 'text'},
            {'name': 'module_id', 'label': 'Module', 'module_id': module_id, 'input_type': 'related', 'related_module_id': module_id, 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'boolean'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def ice_module_subpanels(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'read_only': 1, 'input_type': 'text'},
            {'name': 'label', 'label': 'Label', 'module_id': module_id, 'field_length': 64, 'read_only': 1, 'input_type': 'text'},
            {'name': 'module_id', 'label': 'Module', 'module_id': module_id, 'input_type': 'related', 'related_module_id': module_id, 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'list_size', 'label': 'List Size', 'module_id': module_id, 'input_type': 'text', 'data_type': 'Integer'},
            {'name': 'list_order_column', 'label': 'List Order Column', 'module_id': module_id, 'input_type': 'text'},
            {'name': 'list_order', 'label': 'List Order', 'module_id': module_id, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    
    @staticmethod
    def ice_datalets(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'read_only': 1, 'input_type': 'text'},
            {'name': 'label', 'label': 'Label', 'module_id': module_id, 'field_length': 64, 'read_only': 1, 'input_type': 'text'},
            {'name': 'type', 'label': 'Type', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'field_id', 'label': 'Field ID', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'module_id', 'label': 'Module ID', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'relationship_id', 'label': 'Relationship ID', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'display_order', 'label': 'Display Order', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'type', 'label': 'Type', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'active', 'label': 'Active', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'Boolean'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def ice_users(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'profile_pic', 'label': 'Image', 'module_id': module_id, 'input_type': 'image', 'data_type': 'MEDIUMTEXT'},
            {'name': 'password', 'label': 'Password', 'module_id': module_id, 'field_length': 64, 'input_type': 'password'},
            {'name': 'email', 'label': 'Email', 'module_id': module_id, 'field_length': 32, 'input_type': 'email'},
            {'name': 'role_id', 'label': 'User Role', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('ice_roles'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    @staticmethod
    def ice_roles(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))


    @staticmethod
    def add_datalet_types():
        db.table("ice_datalet_types").delete()

        datalet_types = [
            {'id': 7, 'name': 'CRM Stats'},
            {'id': 8, 'name': 'Totals Report'},
        ]

        for datalet_type in datalet_types:
             db.table('ice_datalet_types').insert(datalet_type)


    @staticmethod
    def add_datalets():
        db.table("ice_datalets").delete()
        datalets = [
            {
                'type': 7,
                'module_id': 2,
                'label': 'CRM Stats',
                'size': 12,
                'display_order': 12,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 8,
                'module_id': 1,
                'label': 'Totals Report',
                'size': 12,
                'display_order': 6,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
        ]

        for datalet in datalets:
            db.table('ice_datalets').insert(datalet)


    @staticmethod
    def currency(module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 32},
            {'name': 'code', 'label': 'Code', 'module_id': module_id, 'field_length': 3},
            {'name': 'symbol', 'label': 'Symbol', 'module_id': module_id, 'field_length': 3}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))


    @staticmethod
    def add_modules_and_roles():
        print ("add modules and roles")
        from iceburgcrm.models.module import Module
        module = Module.where('name', 'ice_roles').first()

        records = db.table(module.name).get()

        db.table('ice_permissions').delete()

        for record in records:
            modules = Module.all()
            for module in modules:
                db.table('ice_permissions').insert({'role_id': record.id, 'module_id': module.id})

    @staticmethod
    def add_workflow_actions():
        db.table('ice_workflow_actions').delete()
        actions = [
            {'name': 'Insert new Module Record'},
            {'name': 'Insert new Relationship Record'},
            {'name': 'Update Module Record'},
            {'name': 'Update Relationship Record'},
            {'name': 'Delete Module Record'},
            {'name': 'Delete Relationship Record'},
            {'name': 'Field Change Status'}
        ]
        for action in actions:
            db.table('ice_workflow_actions').insert(actions)

    @staticmethod
    def add_users():
      
        from faker import Faker
        import bcrypt
        import base64
        from iceburgcrm.models.user import User
        import requests

        faker = Faker()
        User.truncate()

        roles = [
            {'name': 'Admin', 'role_id': 1},
            {'name': 'User', 'role_id': 2},
            {'name': 'Sales', 'role_id': 3},
            {'name': 'Accounting', 'role_id': 4},
            {'name': 'Marketing', 'role_id': 5},
            {'name': 'Support', 'role_id': 6},
            {'name': 'HR', 'role_id': 7}
        ]

        # Generate users for each role
        for role in roles:
            image_url = f"http://demo.iceburg.ca/seed/people/0000{faker.random_int(min=10, max=99)}.jpg"
            image_content = requests.get(image_url).content
            profile_pic = f"data:image/jpg;base64,{base64.b64encode(image_content).decode('utf-8')}"

            password=role['name'].lower()
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')

            db.table('ice_users').insert(
                name=role['name'],
                email=f"{role['name'].lower()}@iceburg.ca",
                profile_pic=profile_pic,
                password=hashed_password_str,
                role_id=role['role_id']
            )

        print("Users added successfully.")

    @staticmethod
    def add_settings():
        from iceburgcrm.models.settings import Setting
        Setting.truncate() 

        # Settings entries
        settings = [
            {'name': 'theme', 'value': 'light'},
            {'name': 'search_per_page', 'value': '10'},
            {'name': 'submodule_search_per_page', 'value': '10'},
            {'name': 'title', 'value': 'Iceburg CRM'},
            {'name': 'description', 'value': 'Open Source, data driven, extendable, unlimited relationships, convertable modules, 29 default themes, light/dark themes'},
            {'name': 'max_export_records', 'value': '10000'},
            {'name': 'welcome_popup', 'value': True},
            {'name': 'currency', 'value': 'USD'},
            {'name': 'language', 'value': 'en'},
            {'name': 'logo', 'value': '0'},
            {'name': 'timezone', 'value': 'UTC'},
            {'name': 'date_format', 'value': 'Y-m-d'},
            {'name': 'time_format', 'value': 'H:i:s'},
            {'name': 'week_start', 'value': 'monday'},
            {'name': 'enable_notifications', 'value': True},
            {'name': 'maintenance_mode', 'value': False},
            {'name': 'api_access', 'value': True},
            {'name': 'auto_backup', 'value': True}
        ]

        for setting in settings:
            db.table('ice_settings').insert(setting)

    @staticmethod
    def add_connectors():
        connector_id = db.table('ice_connectors').insert_get_id({
                                'name': 'joke of the day',
                                'base_url': 'https://official-joke-api.appspot.com'
                            })

        db.table('ice_endpoints').insert(
            connector_id=connector_id,
            endpoint='/random_joke',
            class_name='jokes'
        )

        print("Connectors and endpoints added successfully.")

    @staticmethod
    def ice_roles_data():
        return [
            {'id': 1, 'name': 'Admin'},
            {'id': 2, 'name': 'User'},
            {'id': 3, 'name': 'Sales'},
            {'id': 4, 'name': 'Accounting'},
            {'id': 5, 'name': 'Support'},
            {'id': 6, 'name': 'Marketing'},
            {'id': 7, 'name': 'HR'},
    ]

    '''
    @staticmethod
    def currency_data():
        return [
            {'code': 'AFN', 'name': 'Afghani', 'symbol': '؋'},
            {'code': 'ALL', 'name': 'Lek', 'symbol': 'Lek'},
            {'code': 'ANG', 'name': 'Netherlands Antillian Guilder', 'symbol': 'ƒ'},
            {'code': 'ARS', 'name': 'Argentine Peso', 'symbol': '$'},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': '$'},
            {'code': 'AWG', 'name': 'Aruban Guilder', 'symbol': 'ƒ'},
            {'code': 'AZN', 'name': 'Azerbaijanian Manat', 'symbol': 'ман'},
            {'code': 'BAM', 'name': 'Convertible Marks', 'symbol': 'KM'},
            {'code': 'BDT', 'name': 'Bangladeshi Taka', 'symbol': '৳'},
            {'code': 'BBD', 'name': 'Barbados Dollar', 'symbol': '$'},
            {'code': 'BGN', 'name': 'Bulgarian Lev', 'symbol': 'лв'},
            {'code': 'BMD', 'name': 'Bermudian Dollar', 'symbol': '$'},
            {'code': 'BND', 'name': 'Brunei Dollar', 'symbol': '$'},
            {'code': 'BOB', 'name': 'BOV Boliviano Mvdol', 'symbol': '$b'},
            {'code': 'BRL', 'name': 'Brazilian Real', 'symbol': 'R$'},
            {'code': 'BSD', 'name': 'Bahamian Dollar', 'symbol': '$'},
            {'code': 'BWP', 'name': 'Pula', 'symbol': 'P'},
            {'code': 'BYR', 'name': 'Belarussian Ruble', 'symbol': '₽'},
            {'code': 'BZD', 'name': 'Belize Dollar', 'symbol': 'BZ$'},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': '$'},
            {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'CHF'},
            {'code': 'CLP', 'name': 'CLF Chilean Peso Unidades de fomento', 'symbol': '$'},
            {'code': 'CNY', 'name': 'Yuan Renminbi', 'symbol': '¥'},
            {'code': 'COP', 'name': 'COU Colombian Peso Unidad de Valor Real', 'symbol': '$'},
            {'code': 'CRC', 'name': 'Costa Rican Colon', 'symbol': '₡'},
            {'code': 'CUP', 'name': 'CUC Cuban Peso Peso Convertible', 'symbol': '₱'},
            {'code': 'CZK', 'name': 'Czech Koruna', 'symbol': 'Kč'},
            {'code': 'DKK', 'name': 'Danish Krone', 'symbol': 'kr'},
            {'code': 'DOP', 'name': 'Dominican Peso', 'symbol': 'RD$'},
            {'code': 'EGP', 'name': 'Egyptian Pound', 'symbol': '£'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
            {'code': 'FJD', 'name': 'Fiji Dollar', 'symbol': '$'},
            {'code': 'FKP', 'name': 'Falkland Islands Pound', 'symbol': '£'},
            {'code': 'GBP', 'name': 'Pound Sterling', 'symbol': '£'},
            {'code': 'GIP', 'name': 'Gibraltar Pound', 'symbol': '£'},
            {'code': 'GTQ', 'name': 'Quetzal', 'symbol': 'Q'},
            {'code': 'GYD', 'name': 'Guyana Dollar', 'symbol': '$'},
            {'code': 'HKD', 'name': 'Hong Kong Dollar', 'symbol': '$'},
            {'code': 'HNL', 'name': 'Lempira', 'symbol': 'L'},
            {'code': 'HRK', 'name': 'Croatian Kuna', 'symbol': 'kn'},
            {'code': 'HUF', 'name': 'Forint', 'symbol': 'Ft'},
            {'code': 'IDR', 'name': 'Rupiah', 'symbol': 'Rp'},
            {'code': 'ILS', 'name': 'New Israeli Sheqel', 'symbol': '₪'},
            {'code': 'IRR', 'name': 'Iranian Rial', 'symbol': '﷼'},
            {'code': 'ISK', 'name': 'Iceland Krona', 'symbol': 'kr'},
            {'code': 'JMD', 'name': 'Jamaican Dollar', 'symbol': 'J$'},
            {'code': 'JPY', 'name': 'Yen', 'symbol': '¥'},
            {'code': 'KGS', 'name': 'Som', 'symbol': 'лв'},
            {'code': 'KHR', 'name': 'Riel', 'symbol': '៛'},
            {'code': 'KPW', 'name': 'North Korean Won', 'symbol': '₩'},
            {'code': 'KRW', 'name': 'Won', 'symbol': '₩'},
            {'code': 'KYD', 'name': 'Cayman Islands Dollar', 'symbol': '$'},
            {'code': 'KZT', 'name': 'Tenge', 'symbol': 'лв'},
            {'code': 'LAK', 'name': 'Kip', 'symbol': '₭'},
            {'code': 'LBP', 'name': 'Lebanese Pound', 'symbol': '£'},
            {'code': 'LKR', 'name': 'Sri Lanka Rupee', 'symbol': '₨'},
            {'code': 'LRD', 'name': 'Liberian Dollar', 'symbol': '$'},
            {'code': 'LTL', 'name': 'Lithuanian Litas', 'symbol': 'Lt'},
            {'code': 'LVL', 'name': 'Latvian Lats', 'symbol': 'Ls'},
            {'code': 'MKD', 'name': 'Denar', 'symbol': 'ден'},
            {'code': 'MNT', 'name': 'Tugrik', 'symbol': '₮'},
            {'code': 'MUR', 'name': 'Mauritius Rupee', 'symbol': '₨'},
            {'code': 'MXN', 'name': 'MXV Mexican Peso Mexican Unidad de Inversion (UDI)', 'symbol': '$'},
            {'code': 'MYR', 'name': 'Malaysian Ringgit', 'symbol': 'RM'},
            {'code': 'MZN', 'name': 'Metical', 'symbol': 'MT'},
            {'code': 'NGN', 'name': 'Naira', 'symbol': '₦'},
            {'code': 'NIO', 'name': 'Cordoba Oro', 'symbol': 'C$'},
            {'code': 'NOK', 'name': 'Norwegian Krone', 'symbol': 'kr'},
            {'code': 'NPR', 'name': 'Nepalese Rupee', 'symbol': '₨'},
            {'code': 'NZD', 'name': 'New Zealand Dollar', 'symbol': '$'},
            {'code': 'OMR', 'name': 'Rial Omani', 'symbol': '﷼'},
            {'code': 'PAB', 'name': 'USD Balboa US Dollar', 'symbol': 'B/.'},
            {'code': 'PEN', 'name': 'Nuevo Sol', 'symbol': 'S/.'},
            {'code': 'PHP', 'name': 'Philippine Peso', 'symbol': 'Php'},
            {'code': 'PKR', 'name': 'Pakistan Rupee', 'symbol': '₨'},
            {'code': 'PLN', 'name': 'Zloty', 'symbol': 'zł'},
            {'code': 'PYG', 'name': 'Guarani', 'symbol': 'Gs'},
            {'code': 'QAR', 'name': 'Qatari Rial', 'symbol': '﷼'},
            {'code': 'RON', 'name': 'New Leu', 'symbol': 'lei'},
            {'code': 'RSD', 'name': 'Serbian Dinar', 'symbol': 'Дин.'},
            {'code': 'RUB', 'name': 'Russian Ruble', 'symbol': 'руб'},
            {'code': 'SAR', 'name': 'Saudi Riyal', 'symbol': '﷼'},
            {'code': 'SBD', 'name': 'Solomon Islands Dollar', 'symbol': '$'},
            {'code': 'SCR', 'name': 'Seychelles Rupee', 'symbol': '₨'},
            {'code': 'SEK', 'name': 'Swedish Krona', 'symbol': 'kr'},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': '$'},
            {'code': 'SHP', 'name': 'Saint Helena Pound', 'symbol': '£'},
            {'code': 'SOS', 'name': 'Somali Shilling', 'symbol': 'S'},
            {'code': 'SRD', 'name': 'Surinam Dollar', 'symbol': '$'},
            {'code': 'SVC', 'name': 'USD El Salvador Colon US Dollar', 'symbol': '$'},
            {'code': 'SYP', 'name': 'Syrian Pound', 'symbol': '£'},
            {'code': 'THB', 'name': 'Baht', 'symbol': '฿'},
            {'code': 'TRY', 'name': 'Turkish Lira', 'symbol': 'TL'},
            {'code': 'TTD', 'name': 'Trinidad and Tobago Dollar', 'symbol': 'TT$'},
            {'code': 'TWD', 'name': 'New Taiwan Dollar', 'symbol': 'NT$'},
            {'code': 'UAH', 'name': 'Hryvnia', 'symbol': '₴'},
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
            {'code': 'UYU', 'name': 'UYI Uruguay Peso en Unidades Indexadas', 'symbol': '$U'},
            {'code': 'UZS', 'name': 'Uzbekistan Sum', 'symbol': 'лв'},
            {'code': 'VEF', 'name': 'Bolivar Fuerte', 'symbol': 'Bs'},
            {'code': 'VND', 'name': 'Dong', 'symbol': '₫'},
            {'code': 'XCD', 'name': 'East Caribbean Dollar', 'symbol': '$'},
            {'code': 'YER', 'name': 'Yemeni Rial', 'symbol': '﷼'},
            {'code': 'ZAR', 'name': 'Rand', 'symbol': 'R'}
        ]

    '''


    @staticmethod
    def ice_themes_data():
        return [
            {'name': 'light'},
            {'name': 'dark'},
            {'name': 'cupcake'},
            {'name': 'bumblebee'},
            {'name': 'emerald'},
            {'name': 'corporate'},
            {'name': 'synthwave'},
            {'name': 'retro'},
            {'name': 'cyberpunk'},
            {'name': 'valentine'},
            {'name': 'halloween'},
            {'name': 'garden'},
            {'name': 'forest'},
            {'name': 'aqua'},
            {'name': 'lofi'},
            {'name': 'pastel'},
            {'name': 'fantasy'},
            {'name': 'wireframe'},
            {'name': 'black'},
            {'name': 'luxury'},
            {'name': 'dracula'},
            {'name': 'cmyk'},
            {'name': 'autumn'},
            {'name': 'business'},
            {'name': 'acid'},
            {'name': 'lemonade'},
            {'name': 'night'},
            {'name': 'coffee'},
            {'name': 'winter'},
        ]

    '''
    @staticmethod
    def countries_data():
        return [
            {'code': 'US', 'name': 'Canada'},
            {'code': 'AF', 'name': 'Afghanistan'},
            {'code': 'AL', 'name': 'Albania'},
            {'code': 'DZ', 'name': 'Algeria'},
            {'code': 'AS', 'name': 'American Samoa'},
            {'code': 'AD', 'name': 'Andorra'},
            {'code': 'AO', 'name': 'Angola'},
            {'code': 'AI', 'name': 'Anguilla'},
            {'code': 'AQ', 'name': 'Antarctica'},
            {'code': 'AG', 'name': 'Antigua and/or Barbuda'},
            {'code': 'AR', 'name': 'Argentina'},
            {'code': 'AM', 'name': 'Armenia'},
            {'code': 'AW', 'name': 'Aruba'},
            {'code': 'AU', 'name': 'Australia'},
            {'code': 'AT', 'name': 'Austria'},
            {'code': 'AZ', 'name': 'Azerbaijan'},
            {'code': 'BS', 'name': 'Bahamas'},
            {'code': 'BH', 'name': 'Bahrain'},
            {'code': 'BD', 'name': 'Bangladesh'},
            {'code': 'BB', 'name': 'Barbados'},
            {'code': 'BY', 'name': 'Belarus'},
            {'code': 'BE', 'name': 'Belgium'},
            {'code': 'BZ', 'name': 'Belize'},
            {'code': 'BJ', 'name': 'Benin'},
            {'code': 'BM', 'name': 'Bermuda'},
            {'code': 'BT', 'name': 'Bhutan'},
            {'code': 'BO', 'name': 'Bolivia'},
            {'code': 'BA', 'name': 'Bosnia and Herzegovina'},
            {'code': 'BW', 'name': 'Botswana'},
            {'code': 'BV', 'name': 'Bouvet Island'},
            {'code': 'BR', 'name': 'Brazil'},
            {'code': 'IO', 'name': 'British Indian Ocean Territory'},
            {'code': 'BN', 'name': 'Brunei Darussalam'},
            {'code': 'BG', 'name': 'Bulgaria'},
            {'code': 'BF', 'name': 'Burkina Faso'},
            {'code': 'BI', 'name': 'Burundi'},
            {'code': 'KH', 'name': 'Cambodia'},
            {'code': 'CM', 'name': 'Cameroon'},
            {'code': 'CV', 'name': 'Cape Verde'},
            {'code': 'KY', 'name': 'Cayman Islands'},
            {'code': 'CF', 'name': 'Central African Republic'},
            {'code': 'TD', 'name': 'Chad'},
            {'code': 'CL', 'name': 'Chile'},
            {'code': 'CN', 'name': 'China'},
            {'code': 'CX', 'name': 'Christmas Island'},
            {'code': 'CC', 'name': 'Cocos (Keeling) Islands'},
            {'code': 'CO', 'name': 'Colombia'},
            {'code': 'KM', 'name': 'Comoros'},
            {'code': 'CG', 'name': 'Congo'},
            {'code': 'CK', 'name': 'Cook Islands'},
            {'code': 'CR', 'name': 'Costa Rica'},
            {'code': 'HR', 'name': 'Croatia (Hrvatska)'},
            {'code': 'CU', 'name': 'Cuba'},
            {'code': 'CY', 'name': 'Cyprus'},
            {'code': 'CZ', 'name': 'Czech Republic'},
            {'code': 'DK', 'name': 'Denmark'},
            {'code': 'DJ', 'name': 'Djibouti'},
            {'code': 'DM', 'name': 'Dominica'},
            {'code': 'DO', 'name': 'Dominican Republic'},
            {'code': 'TP', 'name': 'East Timor'},
            {'code': 'EC', 'name': 'Ecuador'},
            {'code': 'EG', 'name': 'Egypt'},
            {'code': 'SV', 'name': 'El Salvador'},
            {'code': 'GQ', 'name': 'Equatorial Guinea'},
            {'code': 'ER', 'name': 'Eritrea'},
            {'code': 'EE', 'name': 'Estonia'},
            {'code': 'ET', 'name': 'Ethiopia'},
            {'code': 'FK', 'name': 'Falkland Islands (Malvinas)'},
            {'code': 'FO', 'name': 'Faroe Islands'},
            {'code': 'FJ', 'name': 'Fiji'},
            {'code': 'FI', 'name': 'Finland'},
            {'code': 'FR', 'name': 'France'},
            {'code': 'FX', 'name': 'France, Metropolitan'},
            {'code': 'GF', 'name': 'French Guiana'},
            {'code': 'PF', 'name': 'French Polynesia'},
            {'code': 'TF', 'name': 'French Southern Territories'},
            {'code': 'GA', 'name': 'Gabon'},
            {'code': 'GM', 'name': 'Gambia'},
            {'code': 'GE', 'name': 'Georgia'},
            {'code': 'DE', 'name': 'Germany'},
            {'code': 'GH', 'name': 'Ghana'},
            {'code': 'GI', 'name': 'Gibraltar'},
            {'code': 'GR', 'name': 'Greece'},
            {'code': 'GL', 'name': 'Greenland'},
            {'code': 'GD', 'name': 'Grenada'},
            {'code': 'GP', 'name': 'Guadeloupe'},
            {'code': 'GU', 'name': 'Guam'},
            {'code': 'GT', 'name': 'Guatemala'},
            {'code': 'GN', 'name': 'Guinea'},
            {'code': 'GW', 'name': 'Guinea-Bissau'},
            {'code': 'GY', 'name': 'Guyana'},
            {'code': 'HT', 'name': 'Haiti'},
            {'code': 'HM', 'name': 'Heard and Mc Donald Islands'},
            {'code': 'HN', 'name': 'Honduras'},
            {'code': 'HK', 'name': 'Hong Kong'},
            {'code': 'HU', 'name': 'Hungary'},
            {'code': 'IS', 'name': 'Iceland'},
            {'code': 'IN', 'name': 'India'},
            {'code': 'ID', 'name': 'Indonesia'},
            {'code': 'IR', 'name': 'Iran (Islamic Republic of)'},
            {'code': 'IQ', 'name': 'Iraq'},
            {'code': 'IE', 'name': 'Ireland'},
            {'code': 'IL', 'name': 'Israel'},
            {'code': 'IT', 'name': 'Italy'},
            {'code': 'CI', 'name': 'Ivory Coast'},
            {'code': 'JM', 'name': 'Jamaica'},
            {'code': 'JP', 'name': 'Japan'},
            {'code': 'JO', 'name': 'Jordan'},
            {'code': 'KZ', 'name': 'Kazakhstan'},
            {'code': 'KE', 'name': 'Kenya'},
            {'code': 'KI', 'name': 'Kiribati'},
            {'code': 'KP', 'name': 'Korea, Democratic People\'s Republic of'},
            {'code': 'KR', 'name': 'Korea, Republic of'},
            {'code': 'KW', 'name': 'Kuwait'},
            {'code': 'KG', 'name': 'Kyrgyzstan'},
            {'code': 'LA', 'name': 'Lao People\'s Democratic Republic'},
            {'code': 'LV', 'name': 'Latvia'},
            {'code': 'LB', 'name': 'Lebanon'},
            {'code': 'LS', 'name': 'Lesotho'},
            {'code': 'LR', 'name': 'Liberia'},
            {'code': 'LY', 'name': 'Libyan Arab Jamahiriya'},
            {'code': 'LI', 'name': 'Liechtenstein'},
            {'code': 'LT', 'name': 'Lithuania'},
            {'code': 'LU', 'name': 'Luxembourg'},
            {'code': 'MO', 'name': 'Macau'},
            {'code': 'MK', 'name': 'Macedonia'},
            {'code': 'MG', 'name': 'Madagascar'},
            {'code': 'MW', 'name': 'Malawi'},
            {'code': 'MY', 'name': 'Malaysia'},
            {'code': 'MV', 'name': 'Maldives'},
            {'code': 'ML', 'name': 'Mali'},
            {'code': 'MT', 'name': 'Malta'},
            {'code': 'MH', 'name': 'Marshall Islands'},
            {'code': 'MQ', 'name': 'Martinique'},
            {'code': 'MR', 'name': 'Mauritania'},
            {'code': 'MU', 'name': 'Mauritius'},
            {'code': 'TY', 'name': 'Mayotte'},
            {'code': 'MX', 'name': 'Mexico'},
            {'code': 'FM', 'name': 'Micronesia, Federated States of'},
            {'code': 'MD', 'name': 'Moldova, Republic of'},
            {'code': 'MC', 'name': 'Monaco'},
            {'code': 'MN', 'name': 'Mongolia'},
            {'code': 'MS', 'name': 'Montserrat'},
            {'code': 'MA', 'name': 'Morocco'},
            {'code': 'MZ', 'name': 'Mozambique'},
            {'code': 'MM', 'name': 'Myanmar'},
            {'code': 'NA', 'name': 'Namibia'},
            {'code': 'NR', 'name': 'Nauru'},
            {'code': 'NP', 'name': 'Nepal'},
            {'code': 'NL', 'name': 'Netherlands'},
            {'code': 'AN', 'name': 'Netherlands Antilles'},
            {'code': 'NC', 'name': 'New Caledonia'},
            {'code': 'NZ', 'name': 'New Zealand'},
            {'code': 'NI', 'name': 'Nicaragua'},
            {'code': 'NE', 'name': 'Niger'},
            {'code': 'NG', 'name': 'Nigeria'},
            {'code': 'NU', 'name': 'Niue'},
            {'code': 'NF', 'name': 'Norfork Island'},
            {'code': 'MP', 'name': 'Northern Mariana Islands'},
            {'code': 'NO', 'name': 'Norway'},
            {'code': 'OM', 'name': 'Oman'},
            {'code': 'PK', 'name': 'Pakistan'},
            {'code': 'PW', 'name': 'Palau'},
            {'code': 'PA', 'name': 'Panama'},
            {'code': 'PG', 'name': 'Papua New Guinea'},
            {'code': 'PY', 'name': 'Paraguay'},
            {'code': 'PE', 'name': 'Peru'},
            {'code': 'PH', 'name': 'Philippines'},
            {'code': 'PN', 'name': 'Pitcairn'},
            {'code': 'PL', 'name': 'Poland'},
            {'code': 'PT', 'name': 'Portugal'},
            {'code': 'PR', 'name': 'Puerto Rico'},
            {'code': 'QA', 'name': 'Qatar'},
            {'code': 'RE', 'name': 'Reunion'},
            {'code': 'RO', 'name': 'Romania'},
            {'code': 'RU', 'name': 'Russian Federation'},
            {'code': 'RW', 'name': 'Rwanda'},
            {'code': 'KN', 'name': 'Saint Kitts and Nevis'},
            {'code': 'LC', 'name': 'Saint Lucia'},
            {'code': 'VC', 'name': 'Saint Vincent and the Grenadines'},
            {'code': 'WS', 'name': 'Samoa'},
            {'code': 'SM', 'name': 'San Marino'},
            {'code': 'ST', 'name': 'Sao Tome and Principe'},
            {'code': 'SA', 'name': 'Saudi Arabia'},
            {'code': 'SN', 'name': 'Senegal'},
            {'code': 'RS', 'name': 'Serbia'},
            {'code': 'SC', 'name': 'Seychelles'},
            {'code': 'SL', 'name': 'Sierra Leone'},
            {'code': 'SG', 'name': 'Singapore'},
            {'code': 'SK', 'name': 'Slovakia'},
            {'code': 'SI', 'name': 'Slovenia'},
            {'code': 'SB', 'name': 'Solomon Islands'},
            {'code': 'SO', 'name': 'Somalia'},
            {'code': 'ZA', 'name': 'South Africa'},
            {'code': 'GS', 'name': 'South Georgia South Sandwich Islands'},
            {'code': 'ES', 'name': 'Spain'},
            {'code': 'LK', 'name': 'Sri Lanka'},
            {'code': 'SH', 'name': 'St. Helena'},
            {'code': 'PM', 'name': 'St. Pierre and Miquelon'},
            {'code': 'SD', 'name': 'Sudan'},
            {'code': 'SR', 'name': 'Suriname'},
            {'code': 'SJ', 'name': 'Svalbarn and Jan Mayen Islands'},
            {'code': 'SZ', 'name': 'Swaziland'},
            {'code': 'SE', 'name': 'Sweden'},
            {'code': 'CH', 'name': 'Switzerland'},
            {'code': 'SY', 'name': 'Syrian Arab Republic'},
            {'code': 'TW', 'name': 'Taiwan'},
            {'code': 'TJ', 'name': 'Tajikistan'},
            {'code': 'TZ', 'name': 'Tanzania, United Republic of'},
            {'code': 'TH', 'name': 'Thailand'},
            {'code': 'TG', 'name': 'Togo'},
            {'code': 'TK', 'name': 'Tokelau'},
            {'code': 'TO', 'name': 'Tonga'},
            {'code': 'TT', 'name': 'Trinidad and Tobago'},
            {'code': 'TN', 'name': 'Tunisia'},
            {'code': 'TR', 'name': 'Turkey'},
            {'code': 'TM', 'name': 'Turkmenistan'},
            {'code': 'TC', 'name': 'Turks and Caicos Islands'},
            {'code': 'TV', 'name': 'Tuvalu'},
            {'code': 'UG', 'name': 'Uganda'},
            {'code': 'UA', 'name': 'Ukraine'},
            {'code': 'AE', 'name': 'United Arab Emirates'},
            {'code': 'GB', 'name': 'United Kingdom'},
            {'code': 'CA', 'name': 'United States'},
            {'code': 'UM', 'name': 'United States minor outlying islands'},
            {'code': 'UY', 'name': 'Uruguay'},
            {'code': 'UZ', 'name': 'Uzbekistan'},
            {'code': 'VU', 'name': 'Vanuatu'},
            {'code': 'VA', 'name': 'Vatican City State'},
            {'code': 'VE', 'name': 'Venezuela'},
            {'code': 'VN', 'name': 'Vietnam'},
            {'code': 'VG', 'name': 'Virgin Islands (British)'},
            {'code': 'VI', 'name': 'Virgin Islands (U.S.)'},
            {'code': 'WF', 'name': 'Wallis and Futuna Islands'},
            {'code': 'EH', 'name': 'Western Sahara'},
            {'code': 'YE', 'name': 'Yemen'},
            {'code': 'YU', 'name': 'Yugoslavia'},
            {'code': 'ZR', 'name': 'Zaire'},
            {'code': 'ZM', 'name': 'Zambia'},
            {'code': 'ZW', 'name': 'Zimbabwe'}
        ]

    @staticmethod
    def states_data():
        return [
            # Canada
            {'code': 'CA', 'abbreviation': 'AB', 'name': 'Alberta'},
            {'code': 'CA', 'abbreviation': 'BC', 'name': 'British Columbia'},
            {'code': 'CA', 'abbreviation': 'MB', 'name': 'Manitoba'},
            {'code': 'CA', 'abbreviation': 'NB', 'name': 'New Brunswick'},
            {'code': 'CA', 'abbreviation': 'NL', 'name': 'Newfoundland and Labrador'},
            {'code': 'CA', 'abbreviation': 'NT', 'name': 'Northwest Territories'},
            {'code': 'CA', 'abbreviation': 'NS', 'name': 'Nova Scotia'},
            {'code': 'CA', 'abbreviation': 'NU', 'name': 'Nunavut'},
            {'code': 'CA', 'abbreviation': 'ON', 'name': 'Ontario'},
            {'code': 'CA', 'abbreviation': 'PE', 'name': 'Prince Edward Island'},
            {'code': 'CA', 'abbreviation': 'QC', 'name': 'Quebec'},
            {'code': 'CA', 'abbreviation': 'SK', 'name': 'Saskatchewan'},
            {'code': 'CA', 'abbreviation': 'YT', 'name': 'Yukon'},

            # USA
            {'code': 'US', 'abbreviation': 'AL', 'name': 'Alabama'},
            {'code': 'US', 'abbreviation': 'AK', 'name': 'Alaska'},
            {'code': 'US', 'abbreviation': 'AZ', 'name': 'Arizona'},
            {'code': 'US', 'abbreviation': 'AR', 'name': 'Arkansas'},
            {'code': 'US', 'abbreviation': 'CA', 'name': 'California'},
            {'code': 'US', 'abbreviation': 'CO', 'name': 'Colorado'},
            {'code': 'US', 'abbreviation': 'CT', 'name': 'Connecticut'},
            {'code': 'US', 'abbreviation': 'DE', 'name': 'Delaware'},
            {'code': 'US', 'abbreviation': 'FL', 'name': 'Florida'},
            {'code': 'US', 'abbreviation': 'GA', 'name': 'Georgia'},
            {'code': 'US', 'abbreviation': 'HI', 'name': 'Hawaii'},
            {'code': 'US', 'abbreviation': 'ID', 'name': 'Idaho'},
            {'code': 'US', 'abbreviation': 'IL', 'name': 'Illinois'},
            {'code': 'US', 'abbreviation': 'IN', 'name': 'Indiana'},
            {'code': 'US', 'abbreviation': 'IA', 'name': 'Iowa'},
            {'code': 'US', 'abbreviation': 'KS', 'name': 'Kansas'},
            {'code': 'US', 'abbreviation': 'KY', 'name': 'Kentucky'},
            {'code': 'US', 'abbreviation': 'LA', 'name': 'Louisiana'},
            {'code': 'US', 'abbreviation': 'ME', 'name': 'Maine'},
            {'code': 'US', 'abbreviation': 'MD', 'name': 'Maryland'},
            {'code': 'US', 'abbreviation': 'MA', 'name': 'Massachusetts'},
            {'code': 'US', 'abbreviation': 'MI', 'name': 'Michigan'},
            {'code': 'US', 'abbreviation': 'MN', 'name': 'Minnesota'},
            {'code': 'US', 'abbreviation': 'MS', 'name': 'Mississippi'},
            {'code': 'US', 'abbreviation': 'MO', 'name': 'Missouri'},
            {'code': 'US', 'abbreviation': 'MT', 'name': 'Montana'},
            {'code': 'US', 'abbreviation': 'NE', 'name': 'Nebraska'},
            {'code': 'US', 'abbreviation': 'NV', 'name': 'Nevada'},
            {'code': 'US', 'abbreviation': 'NH', 'name': 'New Hampshire'},
            {'code': 'US', 'abbreviation': 'NJ', 'name': 'New Jersey'},
            {'code': 'US', 'abbreviation': 'NM', 'name': 'New Mexico'},
            {'code': 'US', 'abbreviation': 'NY', 'name': 'New York'},
            {'code': 'US', 'abbreviation': 'NC', 'name': 'North Carolina'},
            {'code': 'US', 'abbreviation': 'ND', 'name': 'North Dakota'},
            {'code': 'US', 'abbreviation': 'OH', 'name': 'Ohio'},
            {'code': 'US', 'abbreviation': 'OK', 'name': 'Oklahoma'},
            {'code': 'US', 'abbreviation': 'OR', 'name': 'Oregon'},
            {'code': 'US', 'abbreviation': 'PA', 'name': 'Pennsylvania'},
            {'code': 'US', 'abbreviation': 'RI', 'name': 'Rhode Island'},
            {'code': 'US', 'abbreviation': 'SC', 'name': 'South Carolina'},
            {'code': 'US', 'abbreviation': 'SD', 'name': 'South Dakota'},
            {'code': 'US', 'abbreviation': 'TN', 'name': 'Tennessee'},
            {'code': 'US', 'abbreviation': 'TX', 'name': 'Texas'},
            {'code': 'US', 'abbreviation': 'UT', 'name': 'Utah'},
            {'code': 'US', 'abbreviation': 'VT', 'name': 'Vermont'},
            {'code': 'US', 'abbreviation': 'VA', 'name': 'Virginia'},
            {'code': 'US', 'abbreviation': 'WA', 'name': 'Washington'},
            {'code': 'US', 'abbreviation': 'WV', 'name': 'West Virginia'},
            {'code': 'US', 'abbreviation': 'WI', 'name': 'Wisconsin'},
            {'code': 'US', 'abbreviation': 'WY', 'name': 'Wyoming'},
            {'code': 'US', 'abbreviation': 'AS', 'name': 'American Samoa'},
            {'code': 'US', 'abbreviation': 'DC', 'name': 'District of Columbia'},
            {'code': 'US', 'abbreviation': 'GU', 'name': 'Guam'},
            {'code': 'US', 'abbreviation': 'MP', 'name': 'Northern Mariana Islands'},
            {'code': 'US', 'abbreviation': 'PR', 'name': 'Puerto Rico'},
            {'code': 'US', 'abbreviation': 'VI', 'name': 'United States Virgin Islands'},
        ]

    @staticmethod
    def input_type():
        return [
            {'name': 'tel', 'mask': ''},
            {'name': 'email', 'mask': ''},
            {'name': 'city', 'mask': ''},
            {'name': 'custom', 'mask': ''},
            {'name': 'checkbox', 'mask': ''},
            {'name': 'color', 'mask': ''},
            {'name': 'date', 'mask': ''},
            {'name': 'datetime-local', 'mask': ''},
            {'name': 'file', 'mask': ''},
            {'name': 'hidden', 'mask': ''},
            {'name': 'image', 'mask': ''},
            {'name': 'map', 'mask': ''},
            {'name': 'month', 'mask': ''},
            {'name': 'number', 'mask': ''},
            {'name': 'password', 'mask': ''},
            {'name': 'radio', 'mask': ''},
            {'name': 'range', 'mask': ''},
            {'name': 'select', 'mask': ''},
            {'name': 'select_mulitple', 'mask': ''},
            {'name': 'text', 'mask': ''},
            {'name': 'time', 'mask': ''},
            {'name': 'url', 'mask': ''},
            {'name': 'week', 'mask': ''},
            {'name': 'textarea', 'mask': ''},
            {'name': 'video', 'mask': ''},
            {'name': 'zip', 'mask': ''},
            {'name': 'address', 'mask': ''},
            {'name': 'related', 'mask': ''}
        ]

    '''