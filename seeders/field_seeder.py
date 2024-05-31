from orator.seeds import Seeder
from iceburgcrm.models.field import Field
from iceburgcrm.models.module import Module
import logging
import inspect

class FieldSeeder(Seeder):
    def run(self):
        Field.truncate()

        modules = Module.get()
        for module in modules:
            method_name=module.name
            if hasattr(self, method_name):
                logging.info(f'Task Status: Pre {method_name} Generation Started')
                getattr(self, method_name)(module.id)
                logging.info(f'Task Status: {method_name} Generation Completed')
            else:
                logging.info(f'Task Status: {method_name} Generation Skipped - No method')

    
    def ice_modules(self, module_id):
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

    def ice_fields(self, module_id):
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

    def ice_module_subpanels(self, module_id):
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

    

    def ice_datalets(self, module_id):
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

    def ice_users(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'profile_pic', 'label': 'Image', 'module_id': module_id, 'input_type': 'image', 'data_type': 'MEDIUMTEXT'},
            {'name': 'password', 'label': 'Password', 'module_id': module_id, 'field_length': 64, 'input_type': 'password'},
            {'name': 'email', 'label': 'Email', 'module_id': module_id, 'field_length': 32, 'input_type': 'email'},
            {'name': 'role_id', 'label': 'User Role', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('ice_roles'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def ice_roles(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def task_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def task_types(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def case_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def case_priorities(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def project_priorities(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def case_types(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def project_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def project_types(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def quote_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def task_priorities(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def group_types(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def products(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def countries(self, module_id):
        fields = [
            {'name': 'code', 'label': 'Code', 'module_id': module_id, 'field_length': 16},
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 100},
            {'name': 'flag', 'label': 'Flag', 'module_id': module_id, 'input_type': 'image', 'data_type': 'MEDIUMTEXT'}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def currency(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 32},
            {'name': 'code', 'label': 'Code', 'module_id': module_id, 'field_length': 3},
            {'name': 'symbol', 'label': 'Symbol', 'module_id': module_id, 'field_length': 3}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def contract_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 32}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def account_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 32}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def ice_themes(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 32}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    
    def accounts(self, module_id):
        order = 0

        fields = [
            {'name': 'company_logo', 'label': 'Company Logo', 'module_id': module_id, 'input_type': 'image', 'data_type': 'MEDIUMTEXT'},
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'validation': 'required|max:200', 'field_length': 64},
            {'name': 'first_name', 'label': 'First Name', 'module_id': module_id, 'validation': 'required|max:50', 'field_length': 64},
            {'name': 'last_name', 'label': 'Last Name', 'module_id': module_id, 'validation': 'required', 'field_length': 64},
            {'name': 'color', 'label': 'Brand Color', 'module_id': module_id, 'input_type': 'color', 'data_type': 'string'},
            {'name': 'email', 'label': 'Email', 'module_id': module_id, 'field_length': 64, 'input_type': 'email', 'data_type': 'string'},
            {'name': 'fax', 'label': 'Fax', 'module_id': module_id, 'field_length': 32, 'input_type': 'tel'},
            {'name': 'website', 'label': 'Website', 'module_id': module_id, 'field_length': 64, 'input_type': 'url'},
            {'name': 'address', 'label': 'Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'city', 'label': 'City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'zip', 'label': 'Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'state', 'label': 'State', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'country', 'label': 'Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('account_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'}
        ]

        #Field.insert(fields)
        for field in fields:
            Field.insert(Field.get_field(field))
        

  
    def contacts(self, module_id):
        order = 0

        fields = [
            {'name': 'profile_pic', 'label': 'Image', 'module_id': module_id, 'input_type': 'image', 'data_type': 'MEDIUMTEXT'},
            {'name': 'first_name', 'label': 'First Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'last_name', 'label': 'Last Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'email', 'label': 'Email', 'module_id': module_id, 'field_length': 64, 'input_type': 'email'},
            {'name': 'phone', 'label': 'Phone', 'module_id': module_id, 'field_length': 32, 'input_type': 'tel'},
            {'name': 'fax', 'label': 'Fax', 'module_id': module_id, 'field_length': 32, 'input_type': 'tel'},
            {'name': 'website', 'label': 'Website', 'module_id': module_id, 'field_length': 64, 'input_type': 'url'},
            {'name': 'address', 'label': 'Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'city', 'label': 'City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'state', 'label': 'State', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'zip', 'label': 'Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'country', 'label': 'Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('contract_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'email_receive', 'label': 'Email Opt Out', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'boolean'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
        ]



        for field in fields:
            Field.insert(Field.get_field(field))

    def contracts(self, module_id):
        order = 0

        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'discount', 'label': 'Discount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'taxes', 'label': 'Taxes', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'shipping', 'label': 'Shipping', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'subtotal', 'label': 'Subtotal', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'total', 'label': 'Total', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'currency', 'label': 'Currency', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('currency'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'signed_by', 'label': 'Signed By', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('contacts'), 'related_field_id': 'id', 'related_value_id': 'last_name'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'contract_type', 'label': 'Contract Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('contract_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'start_date', 'label': 'Start Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'date'},
            {'name': 'end_date', 'label': 'End Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'date'},
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def lineitems(self, module_id):
        fields = [
            {'name': 'product_id', 'label': 'Product', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('products'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'quantity', 'label': 'Quantity', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'price', 'label': 'Price', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'unit_price', 'label': 'Unit Price', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'cost', 'label': 'Cost', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'discount', 'label': 'Discount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'discount_type', 'label': 'Discount Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('discount_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'taxes', 'label': 'Taxes', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'gross', 'label': 'Gross', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'net', 'label': 'Net', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def opportunities(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'type', 'label': 'Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('opportunity_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'amount', 'label': 'Amount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'probability', 'label': 'Probability', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'close_date', 'label': 'Close Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'date'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('opportunity_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            # {'name': 'sales_stage', 'label': 'Sales Stage', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('sales_stage'), 'related_field_id': 'id', 'related_value_id': 'name'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def orders(self, module_id):
        fields = [
            {'name': 'first_name', 'label': 'First Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'last_name', 'label': 'Last Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'email', 'label': 'Email', 'module_id': module_id, 'field_length': 64, 'input_type': 'email'},
            {'name': 'phone', 'label': 'Phone', 'module_id': module_id, 'field_length': 32, 'input_type': 'tel'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('quote_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'currency', 'label': 'Currency', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('currency'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'amount', 'label': 'Amount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'tax', 'label': 'Tax', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'total', 'label': 'Total', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'subtotal', 'label': 'Subtotal', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'discount', 'label': 'Discount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'billing_address', 'label': 'Billing Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'billing_city', 'label': 'Billing City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'billing_zip', 'label': 'Billing Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'billing_state', 'label': 'Billing State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'billing_country', 'label': 'Billing Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'shipping_address', 'label': 'Shipping Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'shipping_city', 'label': 'Shipping City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'shipping_zip', 'label': 'Shipping Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'shipping_state', 'label': 'Shipping State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'shipping_country', 'label': 'Shipping Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'products', 'label': 'Products', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('products'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def sales(self, module_id):
        fields = [
            {'name': 'total', 'label': 'Total', 'module_id': module_id, 'field_length': 32, 'data_type': 'integer'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def leads(self, module_id):

        fields = [
            {'name': 'first_name', 'label': 'First Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'last_name', 'label': 'Last Name', 'module_id': module_id, 'field_length': 64},
            {'name': 'email', 'label': 'Email', 'module_id': module_id, 'field_length': 64, 'input_type': 'email'},
            {'name': 'phone', 'label': 'Phone', 'module_id': module_id, 'field_length': 32, 'input_type': 'tel'},
            {'name': 'fax', 'label': 'Fax', 'module_id': module_id, 'field_length': 32, 'input_type': 'tel'},
            {'name': 'website', 'label': 'Website', 'module_id': module_id, 'field_length': 64, 'input_type': 'url'},
            {'name': 'address', 'label': 'Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'city', 'label': 'City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'state', 'label': 'State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'zip', 'label': 'Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'country', 'label': 'Country', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('lead_status'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'email_receive', 'label': 'Email Opt Out', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'boolean'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'lead_type', 'label': 'Lead Type', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('lead_types'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'},
            {'name': 'lead_source', 'label': 'Lead Source', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('lead_sources'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'integer'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def ice_relationships(self, module_id):
        order = 0
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'modules', 'label': 'Module List', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'related_field_types', 'label': 'Related Field Types', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'checkbox', 'data_type': 'boolean'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def meetings(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'start_date', 'label': 'Start Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'end_date', 'label': 'End Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'start_time', 'label': 'Start Time', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'end_time', 'label': 'End Time', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'reminder_time', 'label': 'Reminder Time', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'location', 'label': 'Location', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'phone', 'label': 'Phone', 'module_id': module_id, 'field_length': 64, 'input_type': 'tel'},
            {'name': 'link', 'label': 'Link', 'module_id': module_id, 'field_length': 64, 'input_type': 'url'},
            {'name': 'meeting_password', 'label': 'Meeting Password', 'module_id': module_id, 'field_length': 64, 'input_type': 'password'},
            {'name': 'video_recording', 'label': 'Video Recording', 'module_id': module_id, 'input_type': 'video', 'data_type': 'MEDIUMTEXT'},
            {'name': 'audio_recording', 'label': 'Audio Recording', 'module_id': module_id, 'input_type': 'audio', 'data_type': 'MEDIUMTEXT'},
            {'name': 'contract', 'label': 'Contact', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('contacts'), 'related_field_id': 'id', 'related_value_id': 'last_name'},
            {'name': 'types', 'label': 'Types', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('meeting_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('meeting_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def notes(self, module_id):
        fields = [
            {'name': 'subject', 'label': 'Subject', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 190, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def tasks(self, module_id):
        fields = [
            {'name': 'subject', 'label': 'Subject', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 190, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'task_types', 'label': 'Task Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('task_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('task_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'task_priority', 'label': 'Task Priority', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('task_priorities'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'due_date', 'label': 'Due Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def campaigns(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 190, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('campaign_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'budget', 'label': 'Budget', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'forecast', 'label': 'Forecast', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'actual', 'label': 'Actual', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': 8, 'decimal_places': 2},
            {'name': 'impressions', 'label': 'Impressions', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'currency', 'label': 'Currency', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('currency'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'campaign_type', 'label': 'Campaign Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('campaign_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'creative', 'label': 'Creative', 'module_id': module_id, 'input_type': 'video', 'data_type': 'MEDIUMTEXT'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def cases(self, module_id):
        fields = [
            {'name': 'subject', 'label': 'Subject', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 190, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'case_number', 'label': 'Case Number', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('case_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'priority', 'label': 'Priority', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('case_priorities'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'type', 'label': 'Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('case_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'resolution', 'label': 'Resolution', 'module_id': module_id, 'field_length': 190, 'input_type': 'textarea'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def projects(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 64, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 190, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('project_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'priority', 'label': 'Priority', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('project_priorities'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'type', 'label': 'Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('project_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'start_date', 'label': 'Start Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'end_date', 'label': 'End Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'due_date', 'label': 'Due Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'completed_date', 'label': 'Completed Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'estimated_hours', 'label': 'Estimated Hours', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
            {'name': 'actual_hours', 'label': 'Actual Hours', 'module_id': module_id, 'input_type': 'number', 'data_type': 'integer'},
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def quotes(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128, 'input_type': 'text'},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('quote_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'currency', 'label': 'Currency', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('currency'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'amount', 'label': 'Amount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'tax', 'label': 'Tax', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'total', 'label': 'Total', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'subtotal', 'label': 'Subtotal', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'discount', 'label': 'Discount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'billing_address', 'label': 'Billing Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'billing_city', 'label': 'Billing City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'billing_zip', 'label': 'Billing Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'billing_state', 'label': 'Billing State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'billing_country', 'label': 'Billing Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'shipping_address', 'label': 'Shipping Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'shipping_city', 'label': 'Shipping City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'shipping_zip', 'label': 'Shipping Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'shipping_state', 'label': 'Shipping State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'shipping_country', 'label': 'Shipping Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'expire_date', 'label': 'Expire Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))


    def invoices(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('invoice_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'currency', 'label': 'Currency', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('currency'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'amount', 'label': 'Amount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'tax', 'label': 'Tax', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'total', 'label': 'Total', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'subtotal', 'label': 'Subtotal', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'discount', 'label': 'Discount', 'module_id': module_id, 'input_type': 'currency', 'data_type': 'float', 'field_length': '8', 'decimal_places': '2'},
            {'name': 'billing_address', 'label': 'Billing Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'billing_city', 'label': 'Billing City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'billing_zip', 'label': 'Billing Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'billing_state', 'label': 'Billing State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'billing_country', 'label': 'Billing Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'shipping_address', 'label': 'Shipping Address', 'module_id': module_id, 'field_length': 128, 'input_type': 'address'},
            {'name': 'shipping_city', 'label': 'Shipping City', 'module_id': module_id, 'field_length': 64, 'input_type': 'city'},
            {'name': 'shipping_zip', 'label': 'Shipping Zip', 'module_id': module_id, 'field_length': 32, 'input_type': 'zip'},
            {'name': 'shipping_state', 'label': 'Shipping State', 'module_id': module_id, 'input_type': 'related', 'related_module_id': Module.get_id('states'), 'related_field_id': 'id', 'related_value_id': 'name', 'data_type': 'Integer'},
            {'name': 'shipping_country', 'label': 'Shipping Country', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('countries'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'sign_date', 'label': 'Sign Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'expire_date', 'label': 'Expire Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def states(self, module_id):
        fields = [
            {'name': 'code', 'label': 'Code', 'module_id': module_id, 'field_length': 4},
            {'name': 'abbreviation', 'label': 'Abbreviation', 'module_id': module_id, 'field_length': 4},
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 120}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def document_types(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def document_status(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def documents(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128, 'input_type': 'textarea'},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'file_link', 'label': 'Link Url', 'module_id': module_id, 'field_length': 64},
            {'name': 'document_type', 'label': 'Document Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('document_types'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'document_status', 'label': 'Document Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('document_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'expire_date', 'label': 'Expire Date', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def activities(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128},
            {'name': 'assigned_to', 'label': 'Assigned To', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('ice_users'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'date_due', 'label': 'Date Due', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'date_start', 'label': 'Date Start', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'date_finish', 'label': 'Date Finish', 'module_id': module_id, 'input_type': 'date', 'data_type': 'integer'},
            {'name': 'duration', 'label': 'Duration', 'module_id': module_id, 'input_type': 'integer', 'data_type': 'integer'},
            {'name': 'priority', 'label': 'Priority', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('activity_priorities'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'status', 'label': 'Status', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('activity_status'), 'related_field_id': 'id', 'related_value_id': 'name'},
            {'name': 'type', 'label': 'Type', 'module_id': module_id, 'input_type': 'related', 'data_type': 'integer', 'related_module_id': Module.get_id('activity_type'), 'related_field_id': 'id', 'related_value_id': 'name'}
        ]

        for field in fields:
            Field.insert(Field.get_field(field))

    def groups(self, module_id):
        fields = [
            {'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128},
            {'name': 'description', 'label': 'Description', 'module_id': module_id, 'field_length': 128}
        ]
        for field in fields:
            Field.insert(Field.get_field(field))

    def contract_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def discount_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def opportunity_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def opportunity_status(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def lead_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def lead_sources(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def lead_status(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def meeting_status(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def meeting_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def campaign_status(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def campaign_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def meeting_types(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))

    def invoice_status(self, module_id):
        fields = [{'name': 'name', 'label': 'Name', 'module_id': module_id, 'field_length': 128}]
        for field in fields:
            Field.insert(Field.get_field(field))










