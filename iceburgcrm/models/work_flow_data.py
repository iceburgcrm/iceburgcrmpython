from orator import Model
from orator.orm import has_one

class WorkFlowData(Model):
    __table__ = 'ice_work_flow_data'

    @has_one('primary_module_id', 'from_module_id')
    def from_step(self):
        from .module_convertable import ModuleConvertable
        return ModuleConvertable

    @has_one('module_id', 'to_module_id')
    def to_step(self):
        from .module_convertable import ModuleConvertable
        return ModuleConvertable

    @has_one('primary_module_id', 'to_module_id')
    def to_step_primary(self):
        from .module_convertable import ModuleConvertable
        return ModuleConvertable

    @has_one('module_id', 'from_module_id')
    def from_step_primary(self):
        from .module_convertable import ModuleConvertable
        return ModuleConvertable

    @staticmethod
    def get_360_data(module_id, record_id):
        from .module_convertable import ModuleConvertable
        data = {}
        current = WorkFlowData.get_record(module_id, record_id)
        if current:
            data[current.to_module_id] = {
                'module_name': current.to_step_primary.primary_module.name,
                'module_label': current.to_step_primary.primary_module.label,
                'link_id': current.to_id,
                'current': True
            }

            original_module_id, original_record_id = module_id, record_id
            module_id, record_id = current.from_module_id, current.from_id
            while current:
                data[current.to_module_id] = {
                    'module_name': current.to_step_primary.primary_module.name,
                    'module_label': current.to_step_primary.primary_module.label,
                    'link_id': current.to_id
                }
                current = WorkFlowData.get_record(module_id, record_id)
                module_id, record_id = None, None
                if current:
                    module_id, record_id = current.from_module_id, current.from_id
                    
            module_id, record_id = original_module_id, original_record_id
            current = WorkFlowData.get_future_record(module_id, record_id)
            while current:
                data[current.to_module_id] = {
                    'module_name': current.from_step.module.name,
                    'module_label': current.from_step.module.label,
                    'link_id': current.to_id
                }
                current = WorkFlowData.get_future_record(module_id, record_id)
                module_id, record_id = current.to_module_id, current.to_id if current else (None, None)

        steps = ModuleConvertable.where('id', '>', 0).with_('primary_module').order_by('level').get()
        output = [{'step_data': data.get(step.primary_module_id, {'module_name': step.primary_module.name}),
                   'className': 'step-primary' if step.primary_module_id in data else 'step'} for step in steps]

        return output

    @staticmethod
    def get_record(module_id, record_id):
        from .module_convertable import ModuleConvertable
        mc = ModuleConvertable.where('primary_module_id', module_id).select('id').first()
        if mc:
            return WorkFlowData.where('to_id', record_id).where('to_module_id', module_id).first()
        return {}

    @staticmethod
    def get_future_record(module_id, record_id):
        return WorkFlowData.where('from_id', record_id).where('from_module_id', module_id).first()
