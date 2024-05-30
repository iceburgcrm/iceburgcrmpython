from django.http import JsonResponse
from iceburgcrm.models import Module, Schedule, Role, Permission, ModuleSubpanel 
from iceburgcrm.models import Datalet, Relationship, Setting, Connector, Endpoint
from auth_app.admin_decorator import authenticated_user_required
from inertia import render as inertia_render

@authenticated_user_required
def admin_modules(request):
    themes = Module.where('status', 1).get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Modules', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Modules', {'themes': themes, 'breadcrumbs': breadcrumbs})

@authenticated_user_required
def connectors(request):
    connectors = Connector.with_('endpoints').get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Connectors', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Connectors', {'connectors': connectors, 'breadcrumbs': breadcrumbs})

@authenticated_user_required
def admin_data(request):
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Data', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Data', {'breadcrumbs': breadcrumbs})

@authenticated_user_required
def scheduler(request):
    print ('user')
    print (request.oratoruser.id)
    schedule = Schedule.where('user_id', request.oratoruser.id).where('status', 1).get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Scheduler', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Scheduler', {'schedule': schedule, 'breadcrumbs': breadcrumbs})

@authenticated_user_required
def connector_detail(request, connector_id):
    connector = Connector.where('id', connector_id).first().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Connector Detail', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/ConnectorDetail', {'connector': connector, 'breadcrumbs': breadcrumbs})

@authenticated_user_required
def workflow(request):
    permissions = Permission.with_('modules').with_('roles').get().serialize()
    roles = Role.all().serialize()
    modules = Module.where('status', 1).get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Workflow', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Workflow', {
        'permissions': permissions,
        'roles': roles,
        'modules': modules,
        'breadcrumbs': breadcrumbs
    })

@authenticated_user_required
def admin_subpanels(request):
    subpanels = ModuleSubpanel.where('status', 1).get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Subpanels', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Subpanels', {'subpanels': subpanels, 'breadcrumbs': breadcrumbs})

@authenticated_user_required
def admin_datalets(request):
    datalets = Datalet.where('status', 1).get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Datalets', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Datalets', {'datalets': datalets, 'breadcrumbs': breadcrumbs})

@authenticated_user_required
def builder(request):
    modules = Module.where('status', 1).has('subpanels').has('fields').get().serialize()
    datalets = Datalet.all().serialize()
    relationships = Relationship.all().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Builder', 'url': '', 'svg': 'settings'}
    ])
    return inertia_render(request, 'Admin/Builder', {
        'modules': modules,
        'datalets': datalets,
        'relationships': relationships,
        'breadcrumbs': breadcrumbs
    })

@authenticated_user_required
def permissions(request):
    permissions = Permission.with_('modules').with_('roles').get().serialize()
    roles = Role.all().serialize()
    modules = Module.where('status', 1).get().serialize()
    breadcrumbs = Setting.get_breadcrumbs([
        {'name': 'Admin', 'url': '', 'svg': 'admin'},
        {'name': 'Permissions', 'url': '', 'svg': 'settings'}
    ])
    
    return inertia_render(request, 'Admin/Permissions', {
        'permissions': permissions,
        'roles': roles,
        'modules': modules,
        'breadcrumbs': breadcrumbs
    })
