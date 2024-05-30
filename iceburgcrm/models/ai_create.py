import base64
import os
from orator import Model, DatabaseManager, Model
from orator.orm import has_many, belongs_to
from faker import Faker
import json
import logging
import requests
import re

from iceburgcrm.models.field import Field
from iceburgcrm.models.field_seeder import FieldSeeder
from iceburgcrm.models.module import Module
from iceburgcrm.models.module_group import ModuleGroup
from iceburgcrm.models.module_subpanel import ModuleSubpanel
from iceburgcrm.models.relationship import Relationship
from iceburgcrm.models.settings import Setting
from iceburgcrm.models.subpanel_field import SubpanelField
from iceburgcrm.models.field_seeder import FieldSeeder
from auth_app.orator_config import db
from iceburgcrm.models.theme import Theme
from openai import OpenAI





class AICreate():
    
    @staticmethod
    def process(prompt, model="gpt-3.5-turbo", logo=False, seed_amount=0, seed_type=""):
       
        if logo:
            print('Creating logo')
            AICreate.create_logo(prompt)

        print('Updating Settings')
        data=AICreate.get_settings(prompt)
        AICreate.update_settings(data)

        print('Creating Modules')
        modules = AICreate.get_modules(prompt)
        print ("modules", modules)
        AICreate.create_modules(modules)
        if Module.where('primary', 0).count() < 1:
            modules = AICreate.get_modules(prompt)
            AICreate.create_modules(modules)
  
        print("Creating Module Groups")
        module_groups = AICreate.get_module_groups()
        AICreate.create_module_groups(module_groups)
        if ModuleGroup.all().count() < 1:
            AICreate.create_module_groups(module_groups)

        print('Creating Fields')
        for module in Module.where('primary', 0).get():
            AICreate.create_fields(AICreate.get_fields(module), module)

        for module in Module.where('primary', 0).where_doesnt_have('fields').get():
            print(f"Retry fields for {module.name}")
            AICreate.create_fields(AICreate.get_fields(module), module)
        
        print('Creating relationships')
        AICreate.create_relationships(AICreate.get_relationships())

        print('Creating subpanels')
        AICreate.create_subpanels()
        
        print('Generating')
        AICreate.generate(seed_amount)
        print('Done creating')

    @staticmethod
    def get_data(content, no_extract=0):
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        client = OpenAI()
        response = client.chat.completions.create(model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': content}])
        return AICreate.extract_inner_dict(response.choices[0].message.content)
    
    @staticmethod    
    def extract_inner_dict(response):
        logging.debug(f"Raw content to extract: {response}")
        if isinstance(response, str):
            try:
                print ("response1", response)
                response = json.loads(response)
                print ("response", response)
            except json.JSONDecodeError as e:
                print ("ERROR processing")
                logging.error(f"JSON decoding error: {e}")
                return None
        return response

    @staticmethod
    def create_logo(data):
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        client = OpenAI()
        content = f"Give me a dalle-3 prompt for a CRM using the prompt for inspiration and the CRM topic. The artwork should be clean, with no text, allowing the imagery to speak for itself. Prompt: {data}"
        response = AICreate.get_image_data(content)
        if response:
            image_url = response.data[0].url  
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                image_data = image_response.content

                # Encode the image data in base64
                encoded_image = base64.b64encode(image_data).decode('utf-8')
          
                # Update the Setting model with the new image data
                Setting.where('name', 'logo').update({
                    'value': '1',
                    'additional_data': encoded_image
                })
            else:
                print(f"Failed to download the image. Status code: {image_response.status_code}")
        else:
            print("No response received from the AI Create API.")

    @staticmethod
    def get_image_data(content):
        from dotenv import load_dotenv
        load_dotenv()
        OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        client = OpenAI()
        response = client.images.generate(model="dall-e-3",
        prompt=content,
        size="1024x1024",
        quality="standard",
        n=1)
        return AICreate.extract_inner_dict(response)

    @staticmethod
    def generate(seed_amount=0):
        print ("in generate")
        module = Module()
        module.generate(seed_amount)

    @staticmethod
    def generate_ai_records(seed_amount=1, module_id=0, start_at=0):
        for x in range(seed_amount + 1):
            if module_id > 0:
                record = AICreate.get_next_record(module_id)
                AICreate.create_next_record(record, module_id)

    @staticmethod
    def create_next_record(data, module_id):
        if data and 'data' in data:
            module = Module.find(module_id)
            arr = [item['value'] for item in data['data']]
            module.insert_import([arr])
        else:
            print("Data null")
            print(data)

    @staticmethod
    def get_next_record(module_id):
        fields = Field.where('module_id', module_id).get()
        txt = "Fill in the missing value field for the array below."
        for field in fields:
            rules = f"Datatype is: {field.data_type}. Input type is: {field.input_type}. Maximum Field Length is: {field.field_length}."
            txt += f" {{'name': '{field.name}', 'value': '', 'rules': '{rules}'}},"

        module = Module.find(module_id)
        record = module.all().first()
        txt += "\n\nReturn the array with the values field filled in, the name and remove the rules. Output in json (python style - property name enclosed in double quotes). No text explaining."
        return AICreate.get_data(txt)

    @staticmethod
    def create_subpanels():
        relationships = Relationship.where('status', 1).get()
        for relationship in relationships:
            modules = relationship.modules.split(",")
            primary_module = Module.find(modules[0])
            sub_modules = set(modules) - {modules[0]}
            for sub_module_id in sub_modules:
                sub_module = Module.find(sub_module_id)
                subpanel_id = ModuleSubpanel.insert_get_id({
                    'name': f"{primary_module.name}_{sub_module.name}",
                    'label': sub_module.label,
                    'relationship_id': relationship.id,
                    'module_id': primary_module.id
                })
                fields = Field.where('module_id', sub_module_id).get()
                for field in fields.take(3):
                    SubpanelField.insert({
                        'subpanel_id': subpanel_id,
                        'field_id': field.id
                    })

    @staticmethod
    def create_module_groups(data):
        for module_group in data['module_groups']:
            ModuleGroup.insert(module_group)
        for module in data['modules']:
            Module.where('id', module['id']).update({'module_group_id': module['module_group_id']})

    @staticmethod
    def create_modules(data):
        order = 0
        for module in data['modules']:
            module['view_order'] = order
            order += 1
            module['module_group_id'] = 0
            if not Module.where('name', module['name']).first():
                Module.insert(module)

    @staticmethod
    def create_fields(data, module):
       
        if data and 'fields' in data and isinstance(data['fields'], list):
            fields = data['fields']
            for item in fields:
                if 'name' in item and isinstance(item['name'], str):
                    # Lowercase field name to handle created_at or updated_at
                    if item['name'].lower() in ["created_at", "updated_at"]:
                        print(f"Skipping creation or update time field: {item['name']}")
                        continue
                    # Add module id to each item
                    item['module_id'] = module.id
                    # Insert the item into the Field table, handling exceptions
                    try:
                        item=AICreate.check_fields(item, module.id)
                        Field.insert(item)
                    
                    except Exception as e:
                        print ("Exception")
                else:
                    print(f"Missing 'name' or 'name' is not a string in item: {item}")
        else:
            print("Invalid or missing 'fields' key in data")
            

    @staticmethod
    def create_relationships(data):
        print ("in create relationships", data)
        if data:
            for relationship in data:
                relationship['modules'] = ",".join(str(x) for x in relationship['modules'])
                print ("relationship data", relationship)
                Relationship.insert(relationship)

    @staticmethod
    def update_settings(data):
        if data:
            for primary_key, item in data.items():
                if isinstance(item, dict):
                    for key, value in item.items():
                        if isinstance(value, (dict, list)):
                            value = json.dumps(value)
                        Setting.where('name', key).update({'value': value})
        
    @staticmethod
    def get_settings(data):
        themes = db.table("ice_themes").select('name').get().serialize()
        txt = f"Text prompt: {data}\n\n"
        txt += (
            "We're creating a new crm. Based on the prompt text create a title, description and select a theme name.\n\n"
            "List of themes:\n"
            f"{json.dumps(themes, indent=4)}\n\n"
            "Put the theme as a string with a key of theme in the settings array.\n"
            "Put the name as an array key value pair in a settings array.\n"
            "Put the description in the same array using description as the key. The description should be less than 200 characters.\n"
            "JSON encode the array. Provide no text. sample output: \"settings\": {\"title\": \"\",\"description\": \"\", \"theme\": \"\"}"       
        )
        return AICreate.get_data(txt)
    
    @staticmethod  
    def get_modules(data):
  
        modules = Module.where('status', 1).get()

        txt = f"Text prompt: {data}\n\n"
        txt += (
            "User will text in a text prompt. GPT will try to determine a CRM type. Based on the CRM type come up with a list of modules. For example a typical crm may have:\n"
            "Accounts\n"
            "Contacts\n"
            "Contracts\n"
            "Leads\n"
            "Opportunities\n"
            "Lineitems\n"
            "Products\n"
            "Campaigns\n"
            "Cases\n"
            "Documents\n"
            "Notes\n"
            "Projects\n"
            "Groups\n"
            "Quotes\n\n"
            "Include unique Modules that relate to the topic. A book collecting crm might have a books and authors module. A Laravel tutorial crm would have a tutorials module. Find unique modules for the topic.\n\n"
            "For each module create an array like the following format and put all of them in an array under the key modules:\n"
            "[\n"
            "    'name' => 'accounts',\n"
            "    'label' => 'Accounts',\n"
            "    'description' => 'Account module',\n"
            "    'icon' => 'BuildingOffice2Icon',\n"
            "]\n\n"
            "only use these values for the icon\n"
            "'BuildingOffice2Icon',\n"
            "'BuildingOffice2Icon',\n"
            "'BuildingOfficeIcon',\n"
            "'BuildingLibraryIcon',\n"
            "'BuildingStorefrontIcon',\n"
            "'BriefcaseIcon',\n"
            "'HomeIcon',\n"
            "'HomeModernIcon',\n"
            "'UserPlusIcon',\n"
            "'UserMinusIcon',\n"
            "'UserCircleIcon',\n"
            "'UserIcon',\n"
            "'ChatBubbleLeftIcon',\n"
            "'CalculatorIcon',\n"
            "'CircleStackIcon',\n"
            "'BookOpenIcon',\n"
            "'Bars4Icon',\n"
            "'UsersIcon',\n"
            "'LightBulbIcon',\n"
            "'MegaphoneIcon',\n"
            "'InboxStackIcon',\n"
            "'CurrencyDollarIcon',\n"
            "'ArrowRightOnRectangleIcon',\n"
            "'QueueListIcon',\n"
            "'PencilSquareIcon',\n"
            "'DocumentIcon',\n"
            "'PencilIcon',\n"
            "'UserGroupIcon',\n"
            "'GlobeAmericasIcon',\n"
            "'RectangleGroupIcon',\n"
            "'GlobeAltIcon',\n"
            "'CurrencyPoundIcon',\n"
            "'SparklesIcon',\n"
            "'PhoneIcon',\n"
            "'Cog6ToothIcon',\n\n"
            "Output as a json object (python style - property name enclosed in double quotes).\n\n"
            "Do not include any additional text explaining. Try to add at least 15 modules or more. Don't skip any module definition. Don't write 'Follow the pattern above for other modules and fields.', finish the patterns"
        )
        return AICreate.get_data(txt)
    
    @staticmethod
    def create_module_groups(data):
        for module_group in data['module_groups']:
            ModuleGroup.insert(module_group)
        
        for module in data['modules']:
            Module.where('id', module['id']).update({'module_group_id': module['module_group_id']})

    @staticmethod
    def get_module_groups():
        modules = Module.where('status', 1).where('primary', 0).select('id', 'name').get().serialize()

        # Prepare the prompt text
        txt = (
            "\nGroup the following modules into 4 groups for a crm with roughly the same amount in each group. Group them by theme."
            " Save the module_group_id and name in an array with an array key of 'module_groups'. We also want to make another array with"
            " the module_name, module_group_id under the key 'modules' that lists all of the existing modules with the new module_group_id.\n\n"
            " Add name and id of each group to an array under the array key 'module_groups'\n"
            "use this format:\n"
            "[\n"
            "    'id' => '',  // id of the group\n"
            "    'name' => '' // name of group lower case no spaces,\n"
            "    'label' => '',  //label for the group\n"
            "]\n\n"
            "Update the existing module list with the new module_group_id\n"
            "'id', 'module_group_id'\n"
            "[\n"
            "    1, 1\n"
            "]\n\n"
            "list of existing modules:\n"
            f"{json.dumps(modules, indent=4)}\n\n"
            "json encode the array output. Provide no text or explaining."
        )

        return AICreate.get_data(txt)
    
    @staticmethod
    def get_fields(module):
        txt = (
            f"Take the module name '{module.name}' and create a list of crm fields. Try to create at least 15 fields.\n"
            "The format of the array is below. Fill in the missing pieces or remove values depending on the field type\n"
            "[\n"
            "    'name' => '',\n"
            "    'label' => '',\n"
            "    'input_type' => '',\n"
            "]\n\n"
            "rules:\n"
            "input_type can be one of:\n"
            "tel\n"
            "email\n"
            "city\n"
            "custom\n"
            "checkbox\n"
            "color\n"
            "date\n"
            "image\n"
            "number\n"
            "password\n"
            "radio\n"
            "text\n"
            "url\n"
            "textarea\n"
            "video\n"
            "zip\n"
            "address\n\n"
            "output as a json encoded object (python style - property name enclosed in double quotes). No text. No explaining.  Always put the data array under the key fields"
        )

        return AICreate.get_data(txt)

    @staticmethod
    def get_relationships():
        modules = Module.where('primary', 0).select('id', 'name').get().serialize()

        txt = (
            "Below are a list of modules for a CRM. I'm trying to determine if a natural relationship exists between two or more modules. "
            "If it does, I want to make a relationship array item.\n\n"
            "A relationship record looks like for two modules:\n"
            "[\n"
            "    'name' => 'module1name_module2name',\n"
            "    'modules' => [\n"
            "        id of module 1,\n"
            "        id of module 2,\n"
            "    ]\n"
            "]\n"
            "The name is made up of the first module name underscore and the second module name.\n"
            "The ids are made up of the module 1's.\n\n"
            "This is an example of a three module relationship:\n"
            "[\n"
            "    'name' => 'module1name_module2name_module3name',\n"
            "    'modules' => [\n"
            "        id of module 1,\n"
            "        id of module 2,\n"
            "        id of module 3,\n"
            "    ]\n"
            "]\n\n"
            "List of modules:\n"
            f"{json.dumps(modules, indent=4)}\n\n"
            "Go through each module name and ask yourself if this module name is usually related to another module name when thinking about CRMs. Be a little bit creative.\n\n"
            "Try to make 2 or 3 relationships for each module.\n\n"
            "Output each relationship array as a list of arrays JSON encoded (python style - property name enclosed in double quotes). Include no text."
        )
      

        return AICreate.get_data(txt)
    
    @staticmethod
    def check_fields(item, module_id):
        if item is not None: 
            item['module_id'] = module_id
            input_type = item.get('input_type')
            item['data_type']='string'
            if input_type:
                match input_type:
                    case 'tel':
                        item['field_length'] = 32
                    case 'email':
                        item['field_length'] = 64
                    case 'city':
                        item['field_length'] = 50
                    case 'url':
                        item['field_length'] = 75
                    case 'number':
                        item['field_length'] = 0
                        item['data_type'] = 'integer'
                    case 'currency':
                        item['field_length'] = 8
                        item['decimal_places'] = 2
                        item['data_type]'] = 'float'
                    case 'date':
                        item['field_length'] = 0
                        item['data_type'] = 'integer'
                    case 'address':
                        item['field_length'] = 128
                    case 'textarea':
                        item['field_length'] = 190
                    case 'checkbox':
                        item['data_type'] = 'boolean'
                        item['field_length'] = 0
                    case 'password':
                        item['field_length'] = 100
                    case 'text':
                        item['field_length'] = 64
                    case 'video' | 'audio':
                        item['data_type'] = 'mediumtext'
                    case 'zip':
                        item['field_length'] = 20
                    case 'file':
                        item['data_type'] = 'text'
                    case 'number':
                        item['field_length'] = 0
                    case 'related':
                        item['field_length'] = 0
                        item['data_type]'] = 'integer'
                    case _:
                        item['field_length'] = 64

        return item
    