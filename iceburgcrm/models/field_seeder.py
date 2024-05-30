import base64
import random
import string
from faker import Faker
from datetime import datetime, timedelta
from orator.orm import Model
from orator import Schema, DatabaseManager
import requests
from auth_app.orator_config import db

class FieldSeeder:
    def __init__(self, module):
        self.module = module
        self.faker = Faker()

    def seed(self, seed):
        for _ in range(seed):
          
            data = {'ice_slug': ''.join(random.choices(string.ascii_letters + string.digits, k=20))}
            for field in self.module.fields().get():
                if hasattr(field, 'list') and field.list:
                    data[field.name] = 1
                else:
                    data.update(self.generate_field_data(field))

            if 'start_date' in data and 'end_date' in data:
                start_date, end_date = self.handle_dates(self.module.name)
                data['start_date'] = start_date
                data['end_date'] = end_date

            data['created_at'] = datetime.now() - timedelta(days=random.randint(1, 31))
            data['updated_at'] = data['created_at']
        
            id = db.table(self.module.name).insert_get_id(data)
            db.table('ice_work_flow_data').insert({
                'from_id': 0,
                'from_module_id': 0,
                'to_id': id,
                'to_module_id': self.module.id,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            })

    def generate_field_data(self, field):
        data = {}
        if field.input_type == 'color':
            data[field.name] = self.faker.hex_color()
        elif field.input_type == 'tel':
            data[field.name] = self.faker.phone_number()
        elif field.input_type == 'email':
            data[field.name] = self.faker.email()
        elif field.input_type == 'city':
            data[field.name] = self.faker.city()
        elif field.input_type == 'zip':
            data[field.name] = self.faker.postcode()
        elif field.input_type == 'address':
            data[field.name] = self.faker.street_address()
        elif field.input_type == 'checkbox':
            data[field.name] = bool(random.randint(0, 1))
        elif field.input_type == 'file':
            file_content = self.get_sample_file('pdf')
            if file_content:
                data[field.name] = f'data:application/pdf;base64,{file_content}'
        elif field.input_type == 'video':
            data[field.name] = ''
        elif field.input_type == 'audio':
            data[field.name] = ''
        elif field.input_type == 'image':
            image_content = self.get_sample_image(field, data)
            if image_content:
                data[field.name] = f'data:image/jpg;base64,{image_content}'
        elif field.input_type == 'password':
            data[field.name] = self.faker.password()
        elif field.input_type == 'number':
            data[field.name] = random.randint(1, 2000)
        elif field.input_type == 'url':
            data[field.name] = self.faker.url()
        elif field.input_type == 'date':
            data[field.name] = self.faker.date()
        elif field.input_type == 'currency':
            data[field.name] =  round(random.uniform(1, 100), 2)
        elif field.input_type == 'related':
            data[field.name] = random.randint(1, 5)
        elif field.input_type == 'textarea':
            data[field.name] = self.faker.text()
        else:
            if field.name == 'name':
                data[field.name] = self.faker.company()
            elif field.name == 'first_name':
                data[field.name] = self.faker.first_name()
            elif field.name == 'last_name':
                data[field.name] = self.faker.last_name()
            elif field.data_type == 'string':
                data[field.name] = self.faker.text(50)
            elif field.data_type == 'integer':
                data[field.name] = self.faker.random_int(1, 100)
            else:
                data[field.name] = 1

        return data

    def handle_dates(self, module_name):
        start_date = datetime.now()
        end_date = start_date + timedelta(days=random.randint(1, 30))
        return start_date, end_date

    def get_sample_file(self, file_type):
        try:
            file_url = f'http://demo.iceburg.ca/seed/{file_type}/sample.{file_type}'
            file_content = base64.b64encode(requests.get(file_url).content).decode('utf-8')
            return file_content
        except Exception as e:
            print(f"Error fetching file: {e}")
            return None

    def get_sample_image(self, field, data):
        try:
            if field.name == 'flag' and 'code' in data:
                image_url = f'http://demo.iceburg.ca/seed/flags/{data["code"]}.png'
            elif field.name == 'profile_pic':
                image_url = f'http://demo.iceburg.ca/seed/people/0000{random.randint(10, 99)}.jpg'
            elif field.name == 'company_logo':
                image_url = f'http://demo.iceburg.ca/seed/company_logos/{random.randint(1, 23)}.png'
            else:
                return None
            image_content = base64.b64encode(requests.get(image_url).content).decode('utf-8')
            return image_content
        except Exception as e:
            print(f"Error fetching image: {e}")
            return None