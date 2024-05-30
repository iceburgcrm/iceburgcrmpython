from iceburgcrm.models import Datalet, Module, Field, Permission, RelationshipModule
from iceburgcrm.models import Relationship, ModuleSubpanel, Search
from auth_app.decorators import authenticated_user_required
from django.http import JsonResponse, HttpResponse
from django.core.files.temp import NamedTemporaryFile
from auth_app.orator_config import db
import json
import pandas as pd

@authenticated_user_required
def datalet(request):
    datalet_id = request.GET.get('id')
    datalet = Datalet.find_or_fail(datalet_id)
    return JsonResponse(datalet.get_data(), safe=False)

@authenticated_user_required
def delete_record(request, base_id, type):
    if type == 'relationship':
        module_id = RelationshipModule.where('relationship_id', base_id).value('module_id')
    else:
        module_id = base_id

    if not Permission.check_permission(module_id, request.oratoruser, 'write'):
        return JsonResponse({'error': 'No Access'}, status=422)

    status = False
    if type == 'module':
        status = Module.delete_records(base_id, json.loads(request.body))
    elif type == 'relationship':
        status = Relationship.delete_records(base_id, json.loads(request.body))

    return JsonResponse({'success': status}, safe=False)

@authenticated_user_required
def get_record(request, module_id, record_id):
    if not Permission.check_permission(module_id, request.oratoruser):
        return JsonResponse({'error': 'No Access'}, status=422)

    record = Module.get_record(module_id, record_id)
    return JsonResponse(record, safe=False)

@authenticated_user_required
def search_fields(request, value, type):
    module = Module.find_or_fail(value)
    fields = Search.get_fields(module.id, type)
    return JsonResponse(list(fields), safe=False)


@authenticated_user_required
def download(request, module_id, type):
    if not Permission.check_permission(module_id, request.oratoruser, 'export'):
        return JsonResponse({'error': 'No Access'}, status=422)


    if request.body:
        data = Module.get_records(module_id, json.loads(request.body), True)
    else:
        data = Module.get_records(module_id, {}, True) 

    df = pd.DataFrame(data)

    if type in ['xlsx', 'xls']:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        df.to_excel(response, index=False, engine='openpyxl')  # Use 'xlwt' for older xls format
        response['Content-Disposition'] = f'attachment; filename="export.{type}"'
        return response
    elif type == 'csv':
        response = HttpResponse(content_type='text/csv')
        df.to_csv(response, index=False)
        response['Content-Disposition'] = f'attachment; filename="export.csv"'
        return response
    elif type == 'tsv':
        response = HttpResponse(content_type='text/tab-separated-values')
        df.to_csv(response, index=False, sep='\t')  # Set separator to tab for TSV
        response['Content-Disposition'] = f'attachment; filename="export.tsv"'
        return response
    elif type == 'ods':
        response = HttpResponse(content_type='application/vnd.oasis.opendocument.spreadsheet')
        df.to_excel(response, index=False, engine='odf')  # Use 'odf' engine for ODS format
        response['Content-Disposition'] = f'attachment; filename="export.ods"'
        return response
    elif type == 'html':
        response = HttpResponse(df.to_html(), content_type='text/html')
        response['Content-Disposition'] = f'attachment; filename="export.html"'
        return response
    else:
        return JsonResponse({'error': 'Unsupported file format'}, status=400)



@authenticated_user_required
def save_module(request):
    data = json.loads(request.body)
    if not Permission.check_permission(data['module_id'], request.oratoruser, 'write'):
        return JsonResponse({'error': 'No Access'}, status=422)

    result = Module.save_record(data['module_id'], data)
    return JsonResponse(result, safe=False)

@authenticated_user_required
def subpanel_save(request):
    subpanel_id, selected_records, new_records, record_id = ModuleSubpanel.parse_request(request)
    subpanel = ModuleSubpanel.find_or_fail(subpanel_id)
    if not Permission.check_permission(subpanel.module_id, request.oratoruser, 'write'):
        return JsonResponse({'error': 'No Access'}, status=422)

    result = ModuleSubpanel.process_records(subpanel_id, selected_records, new_records, record_id)
    return JsonResponse(result, safe=False)

@authenticated_user_required
def import_module_data(request):
    input_file = request.FILES.get('input_file')
    if not input_file:
        return JsonResponse({'error': 'No file provided'}, status=400)

    with NamedTemporaryFile(delete=True, suffix='.' + input_file.name.split('.')[-1]) as temp_file:
        for chunk in input_file.chunks():
            temp_file.write(chunk)
        temp_file.flush()

        first_row_header = bool(request.POST.get('first_row_header') == 'true')

        if input_file.name.endswith('.xls') or input_file.name.endswith('.xlsx'):
            data = pd.read_excel(temp_file.name, header=0 if first_row_header else None)
        else:
            data = pd.read_csv(temp_file.name, header=0 if first_row_header else None)

    module_id = request.POST.get('module_id')
    if module_id:
        module = Module.where('id', module_id).first()
        if not module or not Permission.check_permission(module.id, request.oratoruser, 'import'):
            return JsonResponse({'error': 'No Access'}, status=422)

        fields = Field.where('module_id', module.id).where('status', 1).get().pluck('name')

    else:
        fields = list(data.columns) 

    if bool(request.POST.get('preview', False)):
        return JsonResponse({
            'preview': 1,
            'fields': list(fields),
            'row': data.iloc[int(first_row_header)].to_dict()  
        })

    data_dicts = data.to_dict(orient='records')
    data = Module.replace_values_for_related_ids(module_id, data_dicts, first_row_header)
    results = Module.insert_import(module, data)

    return JsonResponse({
        'records_updated': len(data),
    })



@authenticated_user_required
def search_data(request):
    params=request.GET.copy()
    data = Search.get_data(request, params)
    return JsonResponse(data, safe=False)

@authenticated_user_required
def ai_assist_fields(request, module_id):
    params=request.GET.copy()
    data = AiAssist.suggest_fields(module_id, params)
    return JsonResponse(data, safe=False)

@authenticated_user_required
def subpanel_data(request, subpanel_id):
    subpanel = ModuleSubpanel.get_subpanel_data(request, subpanel_id, request.GET)
    return JsonResponse(subpanel, safe=False)

@authenticated_user_required
def related_fields(request, field_id):
    field = Field.find_or_fail(field_id)
    related_module = Module.find_or_fail(field.related_module_id)

    records = db.table(related_module.name).select(field.related_field_id, field.related_value_id).get()
    return JsonResponse([record.serialize() for record in records], safe=False)

@authenticated_user_required
def related_field_name(request, field_id, value):
    field = Field.find_or_fail(field_id)
    related_module = Module.find_or_fail(field.related_module_id)
    record = db.table(related_module.name).where(field.related_field_id, value).value(field.related_value_id)
    if not record:
        record = 'Unknown'
    return JsonResponse({'value': record}, safe=False)
