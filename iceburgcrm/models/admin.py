from orator import Model, DatabaseManager
from orator.orm import has_many, belongs_to, has_one
from iceburgcrm.models.module import Module
from iceburgcrm.models.field import Field
from iceburgcrm.models.module_subpanel import ModuleSubpanel
from auth_app.orator_config import db

class Admin:
    def get_data(self, request):
        data = {}
        request_type = request.args.get('type')
        request_id = request.args.get('id')

        if request_type == 'module':
            data = Module.with_('fields', 'groups', 'convertedmodules', 'subpanels').find(request_id)
        elif request_type == 'subpanel':
            data = ModuleSubpanel.with_('relationship.relationshipmodule.module.fields.module', 'module').find(request_id)

        return data

    @staticmethod
    def reset_crm():
        try:
            modules = Module.where('faker_seed', '=', 1).where('admin', '!=', 1).get()
            for module in modules:
                db.table(module.name).truncate()
            return True
        except Exception as e:
            print(str(e)) 
            return False
