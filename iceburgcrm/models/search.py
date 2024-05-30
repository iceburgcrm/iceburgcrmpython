from django.http import JsonResponse
from orator import Model, DatabaseManager
from orator.orm import has_one, belongs_to_many
from iceburgcrm.models.field import Field
from iceburgcrm.models.relationship_module import RelationshipModule
from iceburgcrm.models.relationship import Relationship
from iceburgcrm.models.settings import Setting
from orator.exceptions.orm import ModelNotFound
from auth_app.orator_config import db
from iceburgcrm.models.base import BaseModel

class Search(BaseModel):
    __table__ = 'ice_search'
    
    exclude_field_types = {
        'Search': ['password', 'file', 'image', 'audio', 'video'],
        'OrderBy': ['password', 'image', 'audio', 'video'],
        'Display': ['password'],
        'All': [],
    }

    def get_data(request, params=[], replace_ids=False):
        from .module import Module
        params = Search.initialize_search(params)

        if params['search_type'] == 'relationship':
            results, order_by_field = Search.relationship_search(params)
        else:
            results, order_by_field = Search.module_search(params)

        for key, value in params.items():
            if '__' in key and value not in ['', 'undefined']:
                module_id, field_name = key.split('__', 1)  
                if module_id.isdigit() and int(module_id) > 0:
                    try:
                        field = Field.where('module_id', int(module_id)).where('name', field_name).with_('module').first_or_fail()

                        if field.input_type == 'checkbox':
                            value = 1 if value.lower() == 'true' else 0
                  
                        if field.data_type == 'string':
                            results = results.where(f"{field.module.name}.{field_name}", 'like', f"%{value}%")
                        else:
                            results = results.where(f"{field.module.name}.{field_name}", '=', value)

                    except ModelNotFound:
                        print('Field not found with module_id: {} and name: {}'.format(module_id, field_name))
                        continue  # Skip this iteration and continue processing other parameters

                    
        if not params.get('order_by'):
            params['order_by'] = order_by_field

        pieces = params['order_by'].split('__')
        if len(pieces) > 1 and pieces[0].isdigit():
            module = Module.find_or_fail(int(pieces[0]))
            params['order_by'] = f"{module.name}.{pieces[1]}"

        page = int(params.get('page', 1))
        per_page = int(params.get('per_page', 10))
       
        results = results.order_by(
            params['order_by'], 
            params.get('search_order', 'asc')
        ).paginate(per_page, page)
        
        links = Search.create_pagination_links(request, results)
        data = {
            'data': results.serialize(),
            'links': links,
            'total': results.total,
            'per_page': results.per_page,
            'current_page': results.current_page,
            'last_page': results.last_page
        }
        return data

    def initialize_search(request_data):
        request_data['page'] = int(request_data.get('page', 1))
        request_data['per_page'] = int(request_data.get('per_page', 10))  # Default per page
        request_data['search_order'] = request_data.get('search_order', 'asc')
        request_data['search_type'] = request_data.get('search_type', 'module')
        return request_data
       

    @staticmethod
    def relationship_search(request):
        from .module import Module
        select_fields = []
        order_by_field = ''
        table_primary_ids = ''
        relationship = Relationship.where('name', request.get('relationship_name')) \
                                   .or_where('id', request.get('relationship_id')) \
                                   .first_or_fail()
       
       
        relationship_modules = RelationshipModule.where('relationship_id', relationship.id).select('module_id').get()
        results = db.table(relationship.name)

        for modules in relationship_modules:
            
            join_module = Module.where('id', modules.module_id).first_or_fail()
            fields = Field.where('module_id', join_module.id) \
                          .with_('module', 'related_module') \
                          .get()
            for field in fields:
                select_fields.append(f"{join_module.name}.{field.name} as {join_module.name}__{field.name}")

            results.join(join_module.name, f"{relationship.name}.{join_module.name}_id", '=', f"{join_module.name}.id")
            table_primary_ids += f", {join_module.name}.id as {join_module.name}_row_id"

            order_by_field = f"{join_module.name}_row_id"

            

        select_statement = ', '.join(select_fields) + table_primary_ids + ', ' + relationship.name + '.id as relationship_id'
        results.select_raw(select_statement)

        return results, order_by_field

    @staticmethod
    def module_search(request):
        from .module import Module
        select_fields = []
        select_statement = ""

        module = Module.find_or_fail(int(request.get('module_id')))

        order_by = request.get('order_by', module.primary_field)

        fields = Field.where('module_id', module.id).with_('module', 'related_module').get()

        for field in fields:
            if not request.get('typeahead') or field.input_type in ['text', 'tel', 'email']:
                select_fields.append(f"{module.name}.{field.name} as {module.name}__{field.name}")

        if request.get('typeahead'):
            select_statement = f"{module.primary_field}, "
        
        select_statement += ', '.join(select_fields)
        if select_statement:
            select_statement += ', '

        results = db.table(module.name).select_raw(
            f"{select_statement}{module.name}.{module.primary_field} as {module.name}_row_id"
        )

        order_by_field = f"{module.name}_row_id"

        return results, order_by_field
    
    @staticmethod
    def get_fields(id, search_type='', field_type='All'):
        modules = []

        if search_type == 'relationship':
            relationship = Relationship.where('id', id).first()
            if relationship:
                modules.extend([rm.module_id for rm in relationship.relationshipmodule])
        else:
            modules.append(id)

    
        fields = Field.where_in('module_id', modules).get()
    

        fields = {}
        query = Field.where_in('module_id', modules).where_not_in('input_type', Search.exclude_field_types[field_type])\
        .with_('module')\
        .with_('related_module')


        if field_type == 'Search':
            query.where('search_display', 1).order_by('search_order', 'asc').order_by('id', 'asc')
        elif field_type == 'List':
            query.where('list_display', 1).order_by('display_order', 'asc').order_by('id', 'asc')
        elif field_type == 'Display':
            query.where('list_display', 1).order_by('display_order', 'asc').order_by('id', 'asc')
        elif field_type == 'Edit':
            query.where('edit_display', 1).order_by('edit_order', 'asc').order_by('id', 'asc')

        field_collection = query.get()
     
        for field in field_collection:
            fields[f"{field.id}__{field.name}"] = field.serialize()

        return fields
    
    def create_pagination_links(request, paginated_results):
        query_parameters = request.GET.copy()
        links = {}

        def make_url(page):
            query_parameters['page'] = page
            query_parameters['per_page'] = paginated_results.per_page
            return f"/?{query_parameters.urlencode()}"

        links['first'] = make_url(1)
        links['last'] = make_url(paginated_results.last_page)
        if paginated_results.current_page > 1:
            links['prev'] = make_url(paginated_results.current_page - 1)
        if paginated_results.current_page < paginated_results.last_page:
            links['next'] = make_url(paginated_results.current_page + 1)

        return links
    