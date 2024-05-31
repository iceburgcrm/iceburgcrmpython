import json
from django.http import JsonResponse
from iceburgcrm.models import Permission, Setting, Endpoint, Connector, Admin
from auth_app.admin_decorator import authenticated_user_required

@authenticated_user_required
def module(request):
    data = Admin.get_data(request)  
    return JsonResponse(data, safe=False)

@authenticated_user_required
def permissions_data(request):
    if request.method == "GET":
        permissions = Permission.with_('modules', 'roles').get()
        return JsonResponse([permission.serialize() for permission in permissions], safe=False)
    elif request.method == "POST":
        data = request.POST
        permission = Permission.find(data.get('id', 0))
        if permission:
            permission.can_read = data.get('can_read', permission.can_read)
            permission.can_write = data.get('can_write', permission.can_write)
            permission.can_delete = data.get('can_delete', permission.can_delete)
            permission.save()
            return JsonResponse({'updated': True})
        return JsonResponse({'updated': False}, safe=False)

@authenticated_user_required
def permission_save(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        perm_id = data.get('id', 0)
        perm_type = data.get('type', 'read')
        current_state = data.get('current_state', 0)

        field_name = f'can_{perm_type}'
        field_value = 1 if current_state == 0 else 0

        updated = Permission.where('id', perm_id).update({field_name: field_value})

        if updated:
            return JsonResponse({'status': 'updated'}, safe=False)
        else:
            return JsonResponse({'error': 'No permission found or no update needed'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)

@authenticated_user_required
def builder_data(request, id, type):
    data = {}  
    return JsonResponse(data, safe=False)

@authenticated_user_required
def settings_save(request):
    data = json.loads(request.body)
    result = Setting.save_settings(json.loads(request.body))  
    return JsonResponse(result, safe=False)

@authenticated_user_required
def reset_crm(request):
    status = Admin.reset_crm()  
    return JsonResponse({'status': status}, safe=False)

@authenticated_user_required
def send_request(request):
    result = {}  
    return JsonResponse({'data': result}, safe=False)

@authenticated_user_required
def delete_endpoint(request, endpoint_id):
    Endpoint.find(endpoint_id).delete()
    connectors = Connector.all()
    return JsonResponse([connector.serialize() for connector in connectors], safe=False)

@authenticated_user_required
def delete_connector(request, connector_id):
    Endpoint.where('connector_id', connector_id).delete()
    Connector.find(connector_id).delete()
    return JsonResponse([connector.serialize() for connector in Connector.all()], safe=False)

@authenticated_user_required
def list_connectors(request):
    connectors = Connector.all()
    return JsonResponse([connector.serialize() for connector in connectors], safe=False)
