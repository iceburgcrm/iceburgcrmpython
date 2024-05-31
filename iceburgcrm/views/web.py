from datetime import datetime
from inertia import render as inertia_render
from django.shortcuts import redirect
from iceburgcrm.models import User, Setting, Datalet, Permission, Relationship, Search 
from iceburgcrm.models import ModuleSubpanel, Module, Log, Field, RelationshipModule, WorkFlowData
import requests
from inertia import render
from auth_app.decorators import authenticated_user_required
from auth_app.orator_config import db

@authenticated_user_required
def dashboard(request):
    datalets = Datalet.get_data_all_active_data(request.oratoruser.id)
 
    return inertia_render(request, 'Dashboard', {
        'datalets': datalets
    })

def to_datetime(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
    except (TypeError, ValueError) as e:
        print(f"Error converting timestamp: {e}")
        return None  # or some default

@authenticated_user_required
def calendar(request):
    user_id = request.oratoruser.id
    
    out_meetings = []
    meetings = db.table('meetings').where('assigned_to', user_id).order_by('start_date').get()
    
    for meeting in meetings:
        out_meetings.append({
            'title': meeting['name'],
            'time': {
                'start': to_datetime(meeting['start_date']),
                'end': to_datetime(meeting['end_date'])
            },
            'color': 'yellow',
            'id': meeting['id'],
            'isEditable': False,
            'description': meeting['description'],
        })

    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Calendar', 'url': '', 'svg': 'settings'}
    ])

    return inertia_render(request, 'Calendar', {
        'events': out_meetings,
        'breadcrumbs': breadcrumbs
    })

# Audit Log view
@authenticated_user_required
def audit_log(request, module_id=None):
    if not Permission.check_permission(module_id, request.oratoruser):
        return redirect('dashboard')
   
    module = Module.find(module_id).serialize()
    logs = Log.where('module_id', module_id).with_('user').get().serialize()
    users = User.all().serialize()
    return inertia_render(request, 'Module/AuditLog', {
        'logs': logs,
        'users': users,
        'module': module,
        'permissions': Permission.get_permissions(module_id, request.oratoruser)
    })

# Module Edit view
@authenticated_user_required
def module_edit(request, name, id):
    module = Module.where('name', name).with_('fields').first_or_fail()
    if not Permission.check_permission(module.id, request.oratoruser, 'write'):
        return redirect('dashboard')
    
    from_module=Module.where('id', request.GET.get('from_module', 0)).first()
    from_module_record=Module.get_record(request.GET.get('from_module', 0),request.GET.get('from_id', 0))

    if from_module:
        from_module=from_module.serialize()

    if from_module_record:
        from_module_record=from_module_record.serialize() 

    record = Module.get_record(module.id, id)  

    return inertia_render(request, 'Module/Add', {
        'module': module.serialize(),
        'fields': Field.where('module_id', module.id).with_('module', 'related_module').get().serialize(),
        'record': record,
        'from_module': from_module,
        'from_id': request.GET.get('from_id', 0),
        'type': 'edit',
        'permissions': Permission.get_permissions(module.id, request.oratoruser),
        'convert_from_record': from_module_record,
        'relationships': RelationshipModule.where('module_id', module.id).with_('relationship', 'module_fields').get().serialize(),
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Search ' + module.label, 'url': f'/module/{module.name}', 'svg': 'settings'},
            {'name': 'Edit', 'url': '', 'svg': 'settings'}
        ]),
        'modules': Module.all().serialize(),
    })


# Module View/Edit Combined view
@authenticated_user_required
def module_viewedit(request, module_name, action, record_id):

    module = Module.where('name', module_name).first()

    if action == 'view':
        type="read"
    else:
        type='write'
    if not module or not Permission.check_permission(module.id, request.oratoruser, type):
        return redirect('dashboard')

    record = Module.get_record(module.id, record_id)
    if not record:
        return redirect('dashboard')

    previous, next = Module.get_previous_next(module.id, record_id)
    custom_data = {}

    
    breadcrumbs = Setting.get_breadcrumbs([
            {'name': 'Search', 'url': f'/module/{module.name}', 'svg': 'settings'},
            {'name': action.capitalize(), 'url': '', 'svg': 'settings'},
        ])

    if action == 'view':
        fields=Search.get_fields(module.id, 'module', 'Display')
    else:
        action = 'edit'
        fields=Search.get_fields(module.id, 'module', 'Search')


    return inertia_render(request, f'Module/{action.capitalize()}', {
        'custom_data': custom_data,
        'module': module.serialize(),
        'record': record,
        'next': next,
        'previous': previous,
        'workflow': WorkFlowData.get_360_data(module.id, record_id),
        'field': Field.get_related_field_data(module.id),
        'subpanel_ids': ModuleSubpanel.where('module_id', module.id).select('id').get().serialize(),
        'subpanels': [],
        'fields': fields,
        'permissions': Permission.get_permissions(module.id, request.oratoruser),
        'breadcrumbs': breadcrumbs
    })


# Subpanel Add view
@authenticated_user_required
def subpanel_add(request, subpanel_id):
   
    subpanel = ModuleSubpanel.where('id', subpanel_id).with_('module', 'relationship.relationship_module.module.fields.module').first()

    if not subpanel or not Permission.check_permission(subpanel.module_id, request.oratoruser, 'write'):
        return redirect('dashboard')
    
    from_module_id = request.GET.get('from_module')
    from_module = Module.where('id', from_module_id).first() if from_module_id else None
    from_id = request.GET.get('from_id')

    fields = {}
    if subpanel.relationship and hasattr(subpanel.relationship, 'relationship_module'):
        for item in subpanel.relationship.relationship_module:
            fields[item.module_id] = [field.serialize() for field in Field.where('module_id', item.module_id).with_('module', 'related_module').get()]

    module_name = subpanel.module.name if subpanel.module else 'Unknown'
    breadcrumbs = [
        {'name': 'Search', 'url': f'/module/{module_name}', 'svg': 'settings'},
        {'name': 'Add', 'url': '', 'svg': 'settings'}
    ]

    inertia_data = {
        'subpanel': subpanel.serialize(),
        'fields': fields,
        'from_module': from_module.serialize() if from_module else None,
        'from_id': from_id,
        'breadcrumbs': breadcrumbs,
    }

    return inertia_render(request, 'Subpanel/Add', inertia_data)

@authenticated_user_required
def subpanel_edit(request, subpanel_id, record_id):

    subpanel = ModuleSubpanel.where('id', subpanel_id).with_('module', 'relationship.relationship_module.module.fields.module').first()
    
    if not subpanel or not Permission.check_permission(subpanel.module_id, request.oratoruser, 'write'):
        return redirect('dashboard')

    # Fetch 'from_module' if specified
    from_module_id = request.GET.get('from_module')
    from_module = Module.where('id', from_module_id).first() if from_module_id else None
    from_id = request.GET.get('from_id')

    record = Module.get_record(subpanel.module_id, record_id)

    temp = {}
    temp[1] = 1
    temp[2] = 2

    fields = {}
    if subpanel.relationship and hasattr(subpanel.relationship, 'relationship_module'):
        for item in subpanel.relationship.relationship_module:
            fields[item.module_id] = [field.serialize() for field in Field.where('module_id', item.module_id).with_('module', 'related_module').get()]

    module_name = subpanel.module.name if subpanel.module else 'Unknown'
    breadcrumbs = [
        {'name': 'Search', 'url': f'/module/{module_name}', 'svg': 'settings'},
        {'name': 'Edit', 'url': '', 'svg': 'settings'}
    ]

    inertia_data = {
        'subpanel': subpanel.serialize(),
        'fields': fields,
        'record': record,
        'selected_records': temp,
        'from_module': from_module.serialize() if from_module else None,
        'from_id': from_id,
        'breadcrumbs': breadcrumbs,
    }

    return inertia_render(request, 'Subpanel/Add', inertia_data)

@authenticated_user_required
def relationship_edit(request, name):
    relationship = Relationship.where('name', name).first_or_fail()
    fields = Field.get_fields(relationship.id, 'relationship')
    record = Search.get_data(request, relationship.id, {'search_type': 'relationship'})[0]

    return inertia_render(request, 'Module/Add', {
        'fields': fields,
        'record': record,
        'relationship': relationship,
    })

@authenticated_user_required
def relationship_add(request, name):
    module = Module.where('name', name).with_('fields').first_or_fail()
    if not Permission.check_permission(module.id, request.oratoruser):
        return redirect('dashboard')

    return inertia_render(request, 'Module/Add', {
        'module': module,
        'fields': Field.where('module_id', module.id).with_('module', 'related_module').get(),
        'record': None,
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Search ' + module.label, 'url': f'/module/{module.name}', 'svg': 'settings'},
            {'name': 'Add', 'url': '', 'svg': 'settings'}
        ]),
        'relationship': Relationship.where('name', name).first_or_fail(),
        'relationships': [],
        'modules': Module.all().serialize(),
    })

# Module Add View
@authenticated_user_required
def module_add(request, name):
    module = Module.where('name', name).with_('fields').first_or_fail()
    if not Permission.check_permission(module.id, request.oratoruser, 'write'):
        return redirect('dashboard')
    
    from_module=Module.where('id', request.GET.get('from_module', 0)).first()
    from_module_record=Module.get_record(request.GET.get('from_module', 0),request.GET.get('from_id', 0))

    if from_module:
        from_module=from_module.serialize()

    if from_module_record:
        from_module_record=from_module_record.serialize()   
    

    return inertia_render(request, 'Module/Add', {
        'module': module.serialize(),
        'fields': Field.where('module_id', module.id).with_('module', 'related_module').get().serialize(),
        'record': None,
        'from_module': from_module,
        'from_id': request.GET.get('from_id', 0),
        'type': 'add',
        'permissions': Permission.get_permissions(module.id, request.oratoruser),
        'convert_from_record': from_module_record,
        'relationships': RelationshipModule.where('module_id', module.id).with_('relationship', 'module_fields').get().serialize(),
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Search ' + module.label, 'url': f'/module/{module.name}', 'svg': 'settings'},
            {'name': 'Add', 'url': '', 'svg': 'settings'}
        ]),
        'modules': Module.all().serialize(),
    })

# Module List View
@authenticated_user_required
def module_list(request, module_name):
    
    module = Module.where('name', module_name).with_('fields').first()
    params = request.GET.copy()

    params['module_id'] = module.id  
    params['search_type'] = 'module'

    if not Permission.check_permission(module.id, request.oratoruser):
        return redirect('dashboard')

    relationships = RelationshipModule.where('module_id', module.id).with_('relationship', 'module_fields').get()
    page = db.table(module_name).paginate(3)

  
    return inertia_render(request, 'Module/List', {
        'module': module.serialize(),
        'modules': Module.all().serialize(),
        'field_data': [Field.get_related_field_data(module.id)],
        'records_object': Search.get_data(request, params),
        'page': page.serialize(),
        'request': params,
        'records': Search.get_data(request, params, True),
        'display_fields': Search.get_fields(module.id, 'module','Display'),
        'search_fields': Search.get_fields(module.id, 'module', 'Search'),
        'order_by_fields':Search.get_fields(module.id, 'module', 'OrderBy'),
        'permissions': Permission.get_permissions(module.id, request.oratoruser),
        'relationships': relationships.serialize(),
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Search', 'link': '', 'svg': 'settings'}
        ]),
    })

# Import View
@authenticated_user_required
def import_data(request):
    modules = Module.where('status', 1).get()
    data = {
        'module_id': request.GET.get('from_module_id', request.GET.get('module_id')),
        'module_name': request.GET.get('module_name'),
        'first_row_header': request.GET.get('first_row_header', False)
    }

    return inertia_render(request, 'Import', {
        'modules': modules.serialize(),
        'data': data,
        'from_module_id': request.GET.get('from_module_id'),
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Import', 'link': '', 'svg': 'settings'}
        ]),
    })



# Admin Index View
@authenticated_user_required
def admin_index(request):
    themes = Module.where('status', 1).get()

    return inertia_render(request, 'Admin/Index', {
        'themes': themes,
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Admin', 'link': '', 'svg': 'settings'}
        ]),
    })

# Settings View
@authenticated_user_required
def settings(request):

    if request.oratoruser.role.name != 'Admin':
        return redirect('dashboard')

    themes = Setting.get_themes()

    return inertia_render(request, 'Settings', {
        'settings': 0,
        'themes': themes.serialize(),
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Settings', 'link': '', 'svg': 'settings'}
        ]),
    })

# Modules View
@authenticated_user_required
def modules(request):
    modules = Module.where('status', 1).get()

    return inertia_render(request, 'Modules', {
        'modules': modules,
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Modules', 'link': '', 'svg': 'settings'}
        ]),
    })

# Role Permissions View
@authenticated_user_required
def role_permissions(request):
    if request.oratoruser.role.name != 'Admin':
        return redirect('dashboard')

    return inertia_render(request, 'Searches', {
        'breadcrumbs': Setting.get_breadcrumbs([
            {'name': 'Role Permissions', 'link': '', 'svg': 'settings'}
        ]),
    })

@authenticated_user_required
def all_modules(request):
    modules = Module.where('status', 1).get()

    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Modules', 'link': '', 'svg': 'settings'}
    ])

    return inertia_render(request, 'Modules', {
        'modules': modules.serialize(),
        'breadcrumbs': breadcrumbs
    })


def tos(request):
    user = User.find(1)
    print(user.name)
    return render(request, 'tos', props={
        'terms': 'Here you can place the terms of service text.'
    })

