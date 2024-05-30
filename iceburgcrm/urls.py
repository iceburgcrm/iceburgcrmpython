from django.urls import include, path
from iceburgcrm.views.web import *
from iceburgcrm.views.data import *
from iceburgcrm.views.admin import *
from iceburgcrm.views.admin_data import *



web = [
    path('/', dashboard, name='home'), 
    path('dashboard/', dashboard, name='dashboard'),
    path('calendar', calendar, name='calendar'),
    path('audit_log/<int:module_id>', audit_log, name='audit_log'),
    path('module/<str:name>/edit/<int:id>', module_edit, name='module_edit'),
    path('subpanel/<int:subpanel_id>/edit/<int:record_id>', subpanel_edit, name='subpanel_edit'),
    path('module/<str:module_name>/<str:action>/<int:record_id>', module_viewedit, name='module_viewedit'),
    path('module/<str:module_name>', module_list, name='module_list'),
    path('auth/', include(('auth_app.urls', 'auth_app'), namespace='auth_app')),
    path('subpanel/add/<int:subpanel_id>', subpanel_add, name='subpanel_add'),
    path('relationship/<str:name>/add', relationship_add, name='relationship_add'),
    path('module/<str:name>/add', module_add, name='module_add'),
    path('import', import_data, name='import'),
    path('admin', admin_index, name='admin'),
    path('settings', settings, name='settings'),
    path('modules', all_modules, name='all_modules'),
    path('role_permission', role_permissions, name='role_permissions'),
]


data = [
    path('data/datalet/', datalet, name='datalet'),
    path('data/delete/<int:base_id>/type/<str:type>', delete_record, name='delete_record'),
    path('data/module/<int:module_id>/record/<int:record_id>', get_record, name='get_record'),
    path('data/search_fields/<int:value>/search_type/<str:type>', search_fields, name='relationship_fields'),
    path('data/download/<int:module_id>/<str:type>', download, name='record_save'),
    path('data/save', save_module, name='module_record_save'),
    path('data/subpanel/save', subpanel_save, name='subpanel_record_save'),
    path('data/import', import_module_data, name='module_record_import'),
    path('data/search_data', search_data, name='search_data'),
    path('data/ai_assist/fields/<int:module_id>', ai_assist_fields, name='ai_assist'),
    path('data/subpanel/<int:subpanel_id>', subpanel_data, name='subpanel_relationship_fields'),
    path('data/related_fields/field_id/<int:field_id>', related_fields, name='data_related'),
    path('data/related_field_name/field_id/<int:field_id>/value/<str:value>', related_field_name, name='data_related')
] 


admin = [
    path('admin/modules', admin_modules, name='admin_modules'),
    path('admin/connectors', connectors, name='connectors'),
    path('admin/data', admin_data, name='admin_data'),
    path('admin/scheduler', scheduler, name='scheduler'),
    path('admin/connector/<int:connector_id>', connector_detail, name='connector'),
    path('admin/workflow', workflow, name='permissions'),  
    path('admin/subpanels', admin_subpanels, name='admin_subpanels'),
    path('admin/datalets', admin_datalets, name='admin_datalets'),
    path('admin/builder', builder, name='builder'),
    path('admin/permissions', permissions, name='permissions')
]

admin_data = [
    path('admin/fields', module, name='relationship_fields'),
    path('admin/permissions/data', permissions, name='permissions_data'),
    path('admin/permissions/save', permission_save, name='permission_save'),
    path('admin/builder/<int:id>/type/<str:type>', builder_data, name='builder_data'),
    path('admin/data/settings', settings_save, name='settings_save'),
    path('admin/resetcrm', reset_crm, name='reset_crm'),
    path('admin/sendrequest', send_request, name='send_request'),
    path('admin/connector/delete_endpoint/<int:endpoint_id>', delete_endpoint, name='delete_endpoint'),
    path('admin/connector/delete_connector/<int:connector_id>', delete_connector, name='delete_connector'),
    path('admin/connectors', list_connectors, name='subpanel_relationship_fields')
]

urlpatterns = web + data + admin + admin_data
