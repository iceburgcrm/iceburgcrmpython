from orator.seeds import Seeder
from iceburgcrm.models.module import Module
from iceburgcrm.models.module_group import ModuleGroup
from iceburgcrm.models.module_convertable import ModuleConvertable
import logging

class ModuleSeeder(Seeder):
    def run(self):
        # Truncate existing records to start fresh
        ModuleGroup.truncate()
        Module.truncate()
        ModuleConvertable.truncate()

        # Seed the module groups, modules, and converted modules
        self.seed_module_groups()
        self.seed_modules()
        self.seed_converted_modules()
        logging.info('Modules Seeding Complete')

    def seed_module_groups(self):
        module_groups = [
            {'id': 1, 'name': 'companies', 'label': 'Companies', 'view_order': 0},
            {'id': 2, 'name': 'marketing', 'label': 'Marketing', 'view_order': 0},
            {'id': 3, 'name': 'sales', 'label': 'Sales', 'view_order': 0},
            {'id': 4, 'name': 'communications', 'label': 'Communications', 'view_order': 0},
            {'id': 5, 'name': 'more', 'label': 'More', 'view_order': 0},
            {'id': 6, 'name': 'admin', 'label': 'Admin', 'view_order': 0},
        ]
        ModuleGroup.insert(module_groups)

    def seed_modules(self):
        order = 0
        modules = [
            {'name': 'accounts', 'label': 'Accounts', 'description': 'Account module', 'view_order': order, 'module_group_id': 1, 'icon': 'BuildingOffice2Icon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'contacts', 'label': 'Contacts', 'description': 'Contact module', 'view_order': order+1, 'module_group_id': 1, 'icon': 'UserIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'contracts', 'label': 'Contracts', 'description': 'Contract module', 'view_order': order+2, 'module_group_id': 1, 'icon': 'BookOpenIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'lineitems', 'label': 'Line Items', 'description': 'Line Items module', 'view_order': order+3, 'module_group_id': 3, 'icon': 'Bars4Icon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'leads', 'label': 'Leads', 'description': 'Lead module', 'view_order': order+4, 'module_group_id': 2, 'icon': 'UsersIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'opportunities', 'label': 'Opportunities', 'description': 'Opportunity module', 'view_order': order+5, 'module_group_id': 2, 'icon': 'LightBulbIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'meetings', 'label': 'Meetings', 'description': 'Meetings module', 'view_order': order+6, 'module_group_id': 4, 'icon': 'MegaphoneIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'cases', 'label': 'Cases', 'description': 'Cases module', 'view_order': order+7, 'module_group_id': 2, 'icon': 'InboxStackIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'campaigns', 'label': 'Campaigns', 'description': 'Campaign module', 'view_order': order+8, 'module_group_id': 2, 'icon': 'ArrowRightOnRectangleIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'invoices', 'label': 'Invoices', 'description': 'Invoices module', 'view_order': order+9, 'module_group_id': 3, 'icon': 'CalculatorIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'quotes', 'label': 'Quotes', 'description': 'Quotes module', 'view_order': order+10, 'module_group_id': 3, 'icon': 'QueueListIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'orders', 'label': 'Orders', 'description': 'Orders module', 'view_order': order+11, 'module_group_id': 3, 'icon': 'PencilSquareIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'documents', 'label': 'Documents', 'description': 'Documents module', 'view_order': order+12, 'module_group_id': 5, 'icon': 'DocumentIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'document_types', 'label': 'Document Types', 'description': 'Document Types module', 'view_order': order+13, 'module_group_id': 6, 'icon': 'RectangleGroupIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 0},
            {'name': 'document_status', 'label': 'Document Status', 'description': 'Document Status module', 'view_order': order+14, 'module_group_id': 6, 'icon': 'RectangleGroupIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 0},
            {'name': 'notes', 'label': 'Notes', 'description': 'Notes module', 'view_order': order+15, 'module_group_id': 5, 'icon': 'PencilIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'groups', 'label': 'Groups', 'description': 'Groups module', 'view_order': order+16, 'module_group_id': 5, 'icon': 'UserGroupIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'projects', 'label': 'Projects', 'description': 'Projects module', 'view_order': order+17, 'module_group_id': 5, 'icon': 'RectangleGroupIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'products', 'label': 'Products', 'description': 'Products module', 'view_order': order+18, 'module_group_id': 5, 'icon': 'RectangleGroupIcon', 'status': 1, 'primary': 1, 'create_table': 1, 'faker_seed': 1},
            {'name': 'lead_types', 'label': 'Lead Types', 'description': 'Different types of leads', 'view_order': order+29, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'lead_sources', 'label': 'Lead Sources', 'description': 'Sources of leads', 'view_order': order+30, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'lead_status', 'label': 'Lead Status', 'description': 'Status levels for leads', 'view_order': order+31, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'meeting_status', 'label': 'Meeting Status', 'description': 'Different statuses for meetings', 'view_order': order+32, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'meeting_types', 'label': 'Meeting Types', 'description': 'Types of meetings', 'view_order': order+33, 'module_group_id': 6, 'icon': 'PhoneIcon', 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'campaign_status', 'label': 'Campaign Status', 'description': 'Status levels for marketing campaigns', 'view_order': order+34, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'campaign_types', 'label': 'Campaign Types', 'description': 'Different types of marketing campaigns', 'view_order': order+35, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'tasks', 'label': 'Tasks', 'description': 'Task management', 'view_order': order+36, 'module_group_id': 6, 'icon': 'SparklesIcon', 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 1},
            {'name': 'task_status', 'label': 'Task Status', 'description': 'Different statuses for tasks', 'view_order': order+37, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'task_types', 'label': 'Task Types', 'description': 'Different types of tasks', 'view_order': order+38, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'case_status', 'label': 'Case Status', 'description': 'Status levels for cases', 'view_order': order+39, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'case_priorities', 'label': 'Case Priorities', 'description': 'Priority levels for cases', 'view_order': order+40, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'project_priorities', 'label': 'Project Priorities', 'description': 'Priority levels for projects', 'view_order': order+41, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'case_types', 'label': 'Case Types', 'description': 'Different types of cases', 'view_order': order+42, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'project_status', 'label': 'Project Status', 'description': 'Different statuses for projects', 'view_order': order+43, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'project_types', 'label': 'Project Types', 'description': 'Different types of projects', 'view_order': order+44, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'quote_status', 'label': 'Quote Status', 'description': 'Status levels for quotes', 'view_order': order+45, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'invoice_status', 'label': 'Invoice Status', 'description': 'Status levels for invoices', 'view_order': order+46, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'task_priorities', 'label': 'Task Priorities', 'description': 'Priority levels for tasks', 'view_order': order+47, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'group_types', 'label': 'Group Types', 'description': 'Different types of groups', 'view_order': order+48, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'states', 'label': 'States', 'description': 'Manage different states', 'view_order': order+49, 'module_group_id': 6, 'icon': 'GlobeAmericasIcon', 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'countries', 'label': 'Countries', 'description': 'Manage different countries', 'view_order': order+50, 'module_group_id': 6, 'icon': 'GlobeAltIcon', 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'account_status', 'label': 'Account Status', 'description': 'Status levels for accounts', 'view_order': order+51, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'ice_users', 'label': 'ICE Users', 'description': 'User management for ICE system', 'view_order': order+52, 'module_group_id': 6, 'icon': 'UserPlusIcon', 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0},
            {'name': 'contract_status', 'label': 'Contract Status', 'description': 'Status levels for contracts', 'view_order': order+53, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'ice_roles', 'label': 'ICE Roles', 'description': 'Role management for ICE system', 'view_order': order+54, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'ice_themes', 'label': 'ICE Themes', 'description': 'Theme settings for ICE system', 'view_order': order+55, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_module_subpanels', 'label': 'ICE Module Subpanels', 'description': 'Subpanels within the ICE framework', 'view_order': order+15, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_modules', 'label': 'ICE Modules', 'description': 'Modules within the ICE framework', 'view_order': order+16, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0},
            {'name': 'opportunity_types', 'label': 'Opportunity Types', 'description': 'Different types of opportunities', 'view_order': order+17, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'currency', 'label': 'Currency', 'description': 'Currency management and settings', 'view_order': order+18, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'opportunity_status', 'label': 'Opportunity Status', 'description': 'Status levels for opportunities', 'view_order': order+19, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'ice_fields', 'label': 'ICE Fields', 'description': 'Fields within the ICE framework', 'view_order': order+20, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0},
            {'name': 'ice_datalets', 'label': 'ICE Datalets', 'description': 'Data widgets for ICE dashboards', 'view_order': order+21, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0},
            {'name': 'contract_types', 'label': 'Contract Types', 'description': 'Different types of contracts available', 'view_order': order+22, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'discount_types', 'label': 'Discount Types', 'description': 'Different types of discounts available', 'view_order': order+23, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 1, 'faker_seed': 0},
            {'name': 'ice_relationships', 'label': 'ICE Relationships', 'description': 'Manage relationships within the ICE system', 'view_order': order+24, 'module_group_id': 6, 'icon': None, 'status': 1, 'primary': 0, 'create_table': 0, 'faker_seed': 0}
        ]
                
        Module.insert(modules)

    def seed_converted_modules(self):
        conversions = [
            {'primary_module_id': Module.where('name', 'leads').first().id, 'module_id': Module.where('name', 'contacts').first().id, 'level': 1},
            {'primary_module_id': Module.where('name', 'contacts').first().id, 'module_id': Module.where('name', 'accounts').first().id, 'level': 2},
            {'primary_module_id': Module.where('name', 'accounts').first().id, 'module_id': Module.where('name', 'quotes').first().id, 'level': 3},
            {'primary_module_id': Module.where('name', 'quotes').first().id, 'module_id': Module.where('name', 'opportunities').first().id, 'level': 4},
            {'primary_module_id': Module.where('name', 'opportunities').first().id, 'module_id': Module.where('name', 'contracts').first().id, 'level': 5},
            {'primary_module_id': Module.where('name', 'contracts').first().id, 'module_id': 0, 'level': 6},
        ]
        ModuleConvertable.insert(conversions)
