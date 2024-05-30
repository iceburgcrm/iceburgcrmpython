from orator.orm import has_one
from iceburgcrm.models.datalet_type import DataletType
from auth_app.orator_config import db
from django.utils import timezone
from iceburgcrm.models.base import BaseModel


class Datalet(BaseModel):
    __table__ = 'ice_datalets'  

    @has_one('id', 'type')
    def type(self):
        return DataletType

    @has_one('id', 'module_id')
    def module(self):
        from .module import Module
        return Module

    @has_one('id', 'field_id')
    def field(self):
        from .field import Field
        return Field

    @has_one('id', 'relationship_id')
    def relationship(self):
        from .relationship import Relationship
        return Relationship

    @classmethod
    def get_data_all_active_data(cls, user_role_id):
        results = []
        datalets = cls.where('role_id', 0).or_where('role_id', user_role_id)\
            .with_('type', 'module', 'field', 'relationship')\
            .order_by('display_order').get()

        for datalet in datalets:
            data = {
                'datalet': datalet.serialize(),
                'data': datalet.get_data()
            }
            results.append(data)

        return results

    def get_data(self):
        from iceburgcrm.models.module import Module
        return_data = {}
        now = timezone.now()
   
        if self.type.id == 1:
            return_data = {
                'labels': ['Tax', 'Discount', 'Gross', 'Net'],
                'data': [
                    round(db.table('lineitems').sum('taxes') / 10, 2),
                    round(db.table('lineitems').sum('discount') / 5, 2),
                    db.table('lineitems').sum('gross'),
                    round(db.table('lineitems').sum('gross') / 2, 2),
                ],
            }
        elif self.type.id == 2:
            return_data = {
                'labels': ['Leads', 'Contacts', 'Accounts'],
                'data': [
                    db.table('leads').where('created_at', '>', now - timezone.timedelta(days=7)).count(),
                    db.table('contacts').where('created_at', '>', now - timezone.timedelta(days=7)).count(),
                    db.table('accounts').where('created_at', '>', now - timezone.timedelta(days=7)).count(),
                ],
            }
        elif self.type.id == 3:
            return_data = {
                'labels': ['Today', 'Last 7 Days', 'Last 30 Days'],
                'data': [
                    db.table('meetings').where('created_at', '>', now - timezone.timedelta(days=1)).count(),
                    db.table('meetings').where('created_at', '>', now - timezone.timedelta(days=7)).count(),
                    db.table('meetings').where('created_at', '>', now - timezone.timedelta(days=30)).count(),
                ],
            }
        elif self.type.id == 4:
            return_data = {
                'labels': ['Opportunities', 'Quotes', 'Contracts'],
                'data': [
                    db.table('opportunities').count(),
                    db.table('quotes').count(),
                    db.table('contracts').count(),
                ],
            }
        elif self.type.id == 5:
            return_data = {
                'labels': ['Tax', 'Discount', 'Gross', 'Net'],
                'data': [
                    db.table('invoices').where('created_at', '>', now - timezone.timedelta(days=30)).sum('tax'),
                    db.table('invoices').where('created_at', '>', now - timezone.timedelta(days=30)).sum('discount'),
                    db.table('invoices').where('created_at', '>', now - timezone.timedelta(days=30)).sum('subtotal'),
                    db.table('invoices').where('created_at', '>', now - timezone.timedelta(days=30)).sum('total'),
                ],
            }
        elif self.type.id == 6:
            meeting = db.table('meeting').where('status', '>', 0).order_by('updated_at', 'desc').first()
            if meeting:
                meeting_type_name = db.table('meeting_types').where('id', meeting.types).value('name')   
                meeting.type = meeting_type_name   
                meeting_data = meeting.to_dict()
                
                returnData = [meeting_data]
            
         
                
        elif self.type.id == 7:
            return_data = {
                'modules': db.table('ice_modules').count(),
                'fields': db.table('ice_fields').count(),
                'subpanels': db.table('ice_module_subpanels').count(),
                'relationships': db.table('ice_relationships').count(),
            }

   

        elif self.type.id == 8:
            module_ids = [1, 2, 3, 4, 5]
            class_map = {
                1: 'success',
                2: 'primary',
                3: 'secondary',
                4: 'accident',
                5: 'warning'
            }

            for module_id in module_ids:
                try:

                    module = Module.where('id', module_id).select('name').first()
                    
                    if not module.name:
                        print(f"Module with ID {module_id} not found or has no name.")
                        continue
                  
                    record_count = db.table(module.name).count()

                    return_data[module.name.lower()]={
                        'name': module.name.capitalize(),
                        'value': record_count,
                        'class': class_map.get(module_id, 'default')
                    }
                except Exception as e:
                    print(f"Error processing module ID {module_id}: {e}")


        return return_data
    