import base64
import binascii
import os
import requests
from faker import Faker
import random
from datetime import datetime, timedelta
from django.db import models, transaction
from django.utils.crypto import get_random_string
from iceburgcrm.models.module import Module
from iceburgcrm.models.user import User
from iceburgcrm.models.connector import Connector
from iceburgcrm.models.endpoint import Endpoint
from iceburgcrm.models.datalet import Datalet
from iceburgcrm.models.datalet_type import DataletType
from iceburgcrm.models.permission import Permission
from iceburgcrm.models.settings import Setting
from iceburgcrm.models.work_flow_data import WorkFlowData
import logging
from orator import Model, DatabaseManager
from auth_app.orator_config import db
from orator.seeds import Seeder

logger = logging.getLogger(__name__)

class GenerateSeeder(Seeder):

    def run(self):
        print("Generating users")
        self.add_users()
        print("Generating settings")
        self.add_settings()
        print("Generating connectors")
        self.add_connectors()
        print("Generating datalet types")
        self.add_datalet_types()
        print("Generating datalets")
        self.add_datalets()

    #def add_users(self):
    #    User.truncate()
        # Example of inserting a user, adjust fields as necessary
    #    for _ in range(50):  # Assuming 50 users
    #        image = requests.get(f'http://demo.iceburg.ca/seed/people/0000{random.randint(10, 99)}.jpg').content
    #        User.create(
    #            name='Sample User',
    #            email=f'user{random.randint(1,100)}@example.com',
    #            profile_pic=f'data:image/jpg;base64,{base64.b64encode(image).decode()}',
    #            password='hashed_password',  # Assuming password is already hashed
    #            role_id=random.randint(1,5)  # Assuming roles 1 to 5 exist
    #        )

        seed_amount=50
        Module.generate(seed_amount)
      

        logging.info('Generating static lists')

        faker = Faker()
        modules = db.table('ice_modules').where('status', 1).where('create_table', 1).where('faker_seed', 0).get()

        for module in modules:
            method_name = module.name.lower()
            if hasattr(self, method_name):
                logging.info(f'Generating module: {module.name}')
                table_name = module.name.lower()
                db.table(table_name).truncate()
                data_method = getattr(self, method_name)
                data = data_method()
                for row in data:
                    row['ice_slug'] = get_random_string(32)  # Generates a random hex string
                    db.table(table_name).insert(row)

        self.add_modules_and_roles()
    
    @classmethod
    def add_datalet_types(self):
        db.table("ice_datalet_types").delete()

        datalet_types = [
            {'id': 1, 'name': 'Doughnut Chart'},
            {'id': 2, 'name': 'Line Chart'},
            {'id': 3, 'name': 'Bar Graph'},
            {'id': 4, 'name': 'Pie Chart'},
            {'id': 5, 'name': 'Area Chart'},
            {'id': 6, 'name': 'Latest Meetings'},
            {'id': 7, 'name': 'CRM Stats'},
            {'id': 8, 'name': 'Totals Report'},
        ]

        for datalet_type in datalet_types:
             db.table('ice_datalet_types').insert(datalet_type)


    @classmethod
    def add_datalets(self):
        db.table("ice_datalets").delete()
        datalets = [
            {
                'type': 1,
                'module_id': 0,
                'label': 'Total Sales',
                'size': 12,
                'display_order': 1,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 2,
                'module_id': 0,
                'label': 'Number of new Leads / Contacts / Accounts over the last 7 Days',
                'size': 12,
                'display_order': 2,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 3,
                'module_id': 0,
                'label': 'Meetings',
                'size': 12,
                'display_order': 4,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 4,
                'module_id': 0,
                'label': 'Number of new Opportunities / Quotes / Contracts over the last 7 Days',
                'size': 12,
                'display_order': 5,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 1,
                'module_id': 0,
                'label': 'Orders This Month',
                'size': 12,
                'display_order': 7,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 7,
                'module_id': 2,
                'label': 'CRM Stats',
                'size': 12,
                'display_order': 12,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
            {
                'type': 8,
                'module_id': 1,
                'label': 'Totals Report',
                'size': 12,
                'display_order': 6,
                'created_at': datetime.now(),
                'updated_at': datetime.now()
            },
        ]

        for datalet in datalets:
            db.table('ice_datalets').insert(datalet)


    @classmethod
    def add_modules_and_roles(self):
        module = Module.where('name', 'ice_roles').first()

        records = db.table(module.name).get()

        db.table('ice_permissions').delete()

        for record in records:
            modules = Module.all()
            for module in modules:
                db.table('ice_permissions').insert({'role_id': record.id, 'module_id': module.id})

    @classmethod
    def add_workflow_actions(self):
        db.table('ice_workflow_actions').delete()
        actions = [
            {'name': 'Insert new Module Record'},
            {'name': 'Insert new Relationship Record'},
            {'name': 'Update Module Record'},
            {'name': 'Update Relationship Record'},
            {'name': 'Delete Module Record'},
            {'name': 'Delete Relationship Record'},
            {'name': 'Field Change Status'}
        ]
        for action in actions:
            db.table('ice_workflow_actions').insert(actions)

    @classmethod
    def add_users(self):
        from faker import Faker
        import bcrypt
        import base64

        faker = Faker()
        User.truncate() 

        roles = [
            {'name': 'Admin', 'role_id': 1},
            {'name': 'User', 'role_id': 2},
            {'name': 'Sales', 'role_id': 3},
            {'name': 'Accounting', 'role_id': 4},
            {'name': 'Marketing', 'role_id': 5},
            {'name': 'Support', 'role_id': 6},
            {'name': 'HR', 'role_id': 7}
        ]

        # Generate users for each role
        for role in roles:
            image_url = f"http://demo.iceburg.ca/seed/people/0000{faker.random_int(min=10, max=99)}.jpg"
            image_content = requests.get(image_url).content
            profile_pic = f"data:image/jpg;base64,{base64.b64encode(image_content).decode('utf-8')}"

            password=role['name'].lower()
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            hashed_password_str = hashed_password.decode('utf-8')

            db.table('ice_users').insert(
                name=role['name'],
                email=f"{role['name'].lower()}@iceburg.ca",
                profile_pic=profile_pic,
                password=hashed_password_str,
                role_id=role['role_id']
            )

        print("Users added successfully.")

    @classmethod
    def add_settings(cls):

        Setting.truncate()  
        settings = [
            {'name': 'theme', 'value': 'light'},
            {'name': 'search_per_page', 'value': '10'},
            {'name': 'submodule_search_per_page', 'value': '10'},
            {'name': 'title', 'value': 'Iceburg CRM'},
            {'name': 'description', 'value': 'Open Source, data driven, extendable, unlimited relationships, convertable modules, 29 default themes, light/dark themes'},
            {'name': 'max_export_records', 'value': '10000'},
            {'name': 'welcome_popup', 'value': True},
            {'name': 'currency', 'value': 'USD'},
            {'name': 'language', 'value': 'en'},
            {'name': 'timezone', 'value': 'UTC'},
            {'name': 'date_format', 'value': 'Y-m-d'},
            {'name': 'time_format', 'value': 'H:i:s'},
            {'name': 'week_start', 'value': 'monday'},
            {'name': 'enable_notifications', 'value': True},
            {'name': 'maintenance_mode', 'value': False},
            {'name': 'api_access', 'value': True},
            {'name': 'auto_backup', 'value': True}
        ]

        # Insert settings into the database
        for setting in settings:
            db.table('ice_settings').insert(setting)

    @classmethod
    def add_connectors(self):

        connector_id = db.table('ice_connectors').insert_get_id({
                                'name': 'joke of the day',
                                'base_url': 'https://official-joke-api.appspot.com'
                            })

        db.table('ice_endpoints').insert(
            connector_id=connector_id,
            endpoint='/random_joke',
            class_name='jokes'
        )

        print("Connectors and endpoints added successfully.")

    @staticmethod
    def account_status():
        return [
            {'id': 1, 'name': 'Prospect'},
            {'id': 2, 'name': 'Sold'},
            {'id': 3, 'name': 'Active'},
            {'id': 4, 'name': 'Inactive'},
            {'id': 5, 'name': 'Cancelled'},
            {'id': 6, 'name': 'Closed'},
        ]

    @staticmethod
    def contract_status():
        return [
            {'id': 1, 'name': 'Active'},
            {'id': 2, 'name': 'Inactive'},
            {'id': 3, 'name': 'Pending'},
            {'id': 4, 'name': 'Cancelled'},
            {'id': 5, 'name': 'Suspended'},
            {'id': 6, 'name': 'Terminated'},
            {'id': 7, 'name': 'Deleted'},
        ]

    @staticmethod
    def project_status():
        return [
            {'id': 1, 'name': 'Active'},
            {'id': 2, 'name': 'Inactive'},
            {'id': 3, 'name': 'Pending'},
            {'id': 4, 'name': 'Cancelled'},
            {'id': 5, 'name': 'Suspended'},
            {'id': 6, 'name': 'Terminated'},
            {'id': 7, 'name': 'Deleted'},
        ]
    
    @staticmethod
    def ice_roles():
        return [
            {'id': 1, 'name': 'Admin'},
            {'id': 2, 'name': 'User'},
            {'id': 3, 'name': 'Sales'},
            {'id': 4, 'name': 'Accounting'},
            {'id': 5, 'name': 'Support'},
            {'id': 6, 'name': 'Marketing'},
            {'id': 7, 'name': 'HR'},
    ]

    @staticmethod
    def currency():
        return [
            {'code': 'AFN', 'name': 'Afghani', 'symbol': '؋'},
            {'code': 'ALL', 'name': 'Lek', 'symbol': 'Lek'},
            {'code': 'ANG', 'name': 'Netherlands Antillian Guilder', 'symbol': 'ƒ'},
            {'code': 'ARS', 'name': 'Argentine Peso', 'symbol': '$'},
            {'code': 'AUD', 'name': 'Australian Dollar', 'symbol': '$'},
            {'code': 'AWG', 'name': 'Aruban Guilder', 'symbol': 'ƒ'},
            {'code': 'AZN', 'name': 'Azerbaijanian Manat', 'symbol': 'ман'},
            {'code': 'BAM', 'name': 'Convertible Marks', 'symbol': 'KM'},
            {'code': 'BDT', 'name': 'Bangladeshi Taka', 'symbol': '৳'},
            {'code': 'BBD', 'name': 'Barbados Dollar', 'symbol': '$'},
            {'code': 'BGN', 'name': 'Bulgarian Lev', 'symbol': 'лв'},
            {'code': 'BMD', 'name': 'Bermudian Dollar', 'symbol': '$'},
            {'code': 'BND', 'name': 'Brunei Dollar', 'symbol': '$'},
            {'code': 'BOB', 'name': 'BOV Boliviano Mvdol', 'symbol': '$b'},
            {'code': 'BRL', 'name': 'Brazilian Real', 'symbol': 'R$'},
            {'code': 'BSD', 'name': 'Bahamian Dollar', 'symbol': '$'},
            {'code': 'BWP', 'name': 'Pula', 'symbol': 'P'},
            {'code': 'BYR', 'name': 'Belarussian Ruble', 'symbol': '₽'},
            {'code': 'BZD', 'name': 'Belize Dollar', 'symbol': 'BZ$'},
            {'code': 'CAD', 'name': 'Canadian Dollar', 'symbol': '$'},
            {'code': 'CHF', 'name': 'Swiss Franc', 'symbol': 'CHF'},
            {'code': 'CLP', 'name': 'CLF Chilean Peso Unidades de fomento', 'symbol': '$'},
            {'code': 'CNY', 'name': 'Yuan Renminbi', 'symbol': '¥'},
            {'code': 'COP', 'name': 'COU Colombian Peso Unidad de Valor Real', 'symbol': '$'},
            {'code': 'CRC', 'name': 'Costa Rican Colon', 'symbol': '₡'},
            {'code': 'CUP', 'name': 'CUC Cuban Peso Peso Convertible', 'symbol': '₱'},
            {'code': 'CZK', 'name': 'Czech Koruna', 'symbol': 'Kč'},
            {'code': 'DKK', 'name': 'Danish Krone', 'symbol': 'kr'},
            {'code': 'DOP', 'name': 'Dominican Peso', 'symbol': 'RD$'},
            {'code': 'EGP', 'name': 'Egyptian Pound', 'symbol': '£'},
            {'code': 'EUR', 'name': 'Euro', 'symbol': '€'},
            {'code': 'FJD', 'name': 'Fiji Dollar', 'symbol': '$'},
            {'code': 'FKP', 'name': 'Falkland Islands Pound', 'symbol': '£'},
            {'code': 'GBP', 'name': 'Pound Sterling', 'symbol': '£'},
            {'code': 'GIP', 'name': 'Gibraltar Pound', 'symbol': '£'},
            {'code': 'GTQ', 'name': 'Quetzal', 'symbol': 'Q'},
            {'code': 'GYD', 'name': 'Guyana Dollar', 'symbol': '$'},
            {'code': 'HKD', 'name': 'Hong Kong Dollar', 'symbol': '$'},
            {'code': 'HNL', 'name': 'Lempira', 'symbol': 'L'},
            {'code': 'HRK', 'name': 'Croatian Kuna', 'symbol': 'kn'},
            {'code': 'HUF', 'name': 'Forint', 'symbol': 'Ft'},
            {'code': 'IDR', 'name': 'Rupiah', 'symbol': 'Rp'},
            {'code': 'ILS', 'name': 'New Israeli Sheqel', 'symbol': '₪'},
            {'code': 'IRR', 'name': 'Iranian Rial', 'symbol': '﷼'},
            {'code': 'ISK', 'name': 'Iceland Krona', 'symbol': 'kr'},
            {'code': 'JMD', 'name': 'Jamaican Dollar', 'symbol': 'J$'},
            {'code': 'JPY', 'name': 'Yen', 'symbol': '¥'},
            {'code': 'KGS', 'name': 'Som', 'symbol': 'лв'},
            {'code': 'KHR', 'name': 'Riel', 'symbol': '៛'},
            {'code': 'KPW', 'name': 'North Korean Won', 'symbol': '₩'},
            {'code': 'KRW', 'name': 'Won', 'symbol': '₩'},
            {'code': 'KYD', 'name': 'Cayman Islands Dollar', 'symbol': '$'},
            {'code': 'KZT', 'name': 'Tenge', 'symbol': 'лв'},
            {'code': 'LAK', 'name': 'Kip', 'symbol': '₭'},
            {'code': 'LBP', 'name': 'Lebanese Pound', 'symbol': '£'},
            {'code': 'LKR', 'name': 'Sri Lanka Rupee', 'symbol': '₨'},
            {'code': 'LRD', 'name': 'Liberian Dollar', 'symbol': '$'},
            {'code': 'LTL', 'name': 'Lithuanian Litas', 'symbol': 'Lt'},
            {'code': 'LVL', 'name': 'Latvian Lats', 'symbol': 'Ls'},
            {'code': 'MKD', 'name': 'Denar', 'symbol': 'ден'},
            {'code': 'MNT', 'name': 'Tugrik', 'symbol': '₮'},
            {'code': 'MUR', 'name': 'Mauritius Rupee', 'symbol': '₨'},
            {'code': 'MXN', 'name': 'MXV Mexican Peso Mexican Unidad de Inversion (UDI)', 'symbol': '$'},
            {'code': 'MYR', 'name': 'Malaysian Ringgit', 'symbol': 'RM'},
            {'code': 'MZN', 'name': 'Metical', 'symbol': 'MT'},
            {'code': 'NGN', 'name': 'Naira', 'symbol': '₦'},
            {'code': 'NIO', 'name': 'Cordoba Oro', 'symbol': 'C$'},
            {'code': 'NOK', 'name': 'Norwegian Krone', 'symbol': 'kr'},
            {'code': 'NPR', 'name': 'Nepalese Rupee', 'symbol': '₨'},
            {'code': 'NZD', 'name': 'New Zealand Dollar', 'symbol': '$'},
            {'code': 'OMR', 'name': 'Rial Omani', 'symbol': '﷼'},
            {'code': 'PAB', 'name': 'USD Balboa US Dollar', 'symbol': 'B/.'},
            {'code': 'PEN', 'name': 'Nuevo Sol', 'symbol': 'S/.'},
            {'code': 'PHP', 'name': 'Philippine Peso', 'symbol': 'Php'},
            {'code': 'PKR', 'name': 'Pakistan Rupee', 'symbol': '₨'},
            {'code': 'PLN', 'name': 'Zloty', 'symbol': 'zł'},
            {'code': 'PYG', 'name': 'Guarani', 'symbol': 'Gs'},
            {'code': 'QAR', 'name': 'Qatari Rial', 'symbol': '﷼'},
            {'code': 'RON', 'name': 'New Leu', 'symbol': 'lei'},
            {'code': 'RSD', 'name': 'Serbian Dinar', 'symbol': 'Дин.'},
            {'code': 'RUB', 'name': 'Russian Ruble', 'symbol': 'руб'},
            {'code': 'SAR', 'name': 'Saudi Riyal', 'symbol': '﷼'},
            {'code': 'SBD', 'name': 'Solomon Islands Dollar', 'symbol': '$'},
            {'code': 'SCR', 'name': 'Seychelles Rupee', 'symbol': '₨'},
            {'code': 'SEK', 'name': 'Swedish Krona', 'symbol': 'kr'},
            {'code': 'SGD', 'name': 'Singapore Dollar', 'symbol': '$'},
            {'code': 'SHP', 'name': 'Saint Helena Pound', 'symbol': '£'},
            {'code': 'SOS', 'name': 'Somali Shilling', 'symbol': 'S'},
            {'code': 'SRD', 'name': 'Surinam Dollar', 'symbol': '$'},
            {'code': 'SVC', 'name': 'USD El Salvador Colon US Dollar', 'symbol': '$'},
            {'code': 'SYP', 'name': 'Syrian Pound', 'symbol': '£'},
            {'code': 'THB', 'name': 'Baht', 'symbol': '฿'},
            {'code': 'TRY', 'name': 'Turkish Lira', 'symbol': 'TL'},
            {'code': 'TTD', 'name': 'Trinidad and Tobago Dollar', 'symbol': 'TT$'},
            {'code': 'TWD', 'name': 'New Taiwan Dollar', 'symbol': 'NT$'},
            {'code': 'UAH', 'name': 'Hryvnia', 'symbol': '₴'},
            {'code': 'USD', 'name': 'US Dollar', 'symbol': '$'},
            {'code': 'UYU', 'name': 'UYI Uruguay Peso en Unidades Indexadas', 'symbol': '$U'},
            {'code': 'UZS', 'name': 'Uzbekistan Sum', 'symbol': 'лв'},
            {'code': 'VEF', 'name': 'Bolivar Fuerte', 'symbol': 'Bs'},
            {'code': 'VND', 'name': 'Dong', 'symbol': '₫'},
            {'code': 'XCD', 'name': 'East Caribbean Dollar', 'symbol': '$'},
            {'code': 'YER', 'name': 'Yemeni Rial', 'symbol': '﷼'},
            {'code': 'ZAR', 'name': 'Rand', 'symbol': 'R'}
        ]

    @staticmethod
    def ice_themes():
        return [
            {'name': 'light'},
            {'name': 'dark'},
            {'name': 'cupcake'},
            {'name': 'bumblebee'},
            {'name': 'emerald'},
            {'name': 'corporate'},
            {'name': 'synthwave'},
            {'name': 'retro'},
            {'name': 'cyberpunk'},
            {'name': 'valentine'},
            {'name': 'halloween'},
            {'name': 'garden'},
            {'name': 'forest'},
            {'name': 'aqua'},
            {'name': 'lofi'},
            {'name': 'pastel'},
            {'name': 'fantasy'},
            {'name': 'wireframe'},
            {'name': 'black'},
            {'name': 'luxury'},
            {'name': 'dracula'},
            {'name': 'cmyk'},
            {'name': 'autumn'},
            {'name': 'business'},
            {'name': 'acid'},
            {'name': 'lemonade'},
            {'name': 'night'},
            {'name': 'coffee'},
            {'name': 'winter'},
        ]

    @staticmethod
    def contract_types():
        return [
            {'id': 1, 'name': 'Sale'},
            {'id': 2, 'name': 'Rental'},
            {'id': 3, 'name': 'Lease'},
            {'id': 4, 'name': 'Purchase'},
            {'id': 5, 'name': 'Other'},
        ]

    @staticmethod
    def document_types():
        return [
            {'id': 1, 'name': 'Text'},
            {'id': 2, 'name': 'Word'},
            {'id': 3, 'name': 'PDF'},
            {'id': 4, 'name': 'Open Office'},
            {'id': 5, 'name': 'Other'},
        ]
    
    @staticmethod
    def project_types():
        return [
            {'id': 1, 'name': 'Feature'},
            {'id': 2, 'name': 'Bug'},
            {'id': 3, 'name': 'Other'},
        ]

    @staticmethod
    def contract_terms():
        return [
            {'id': 1, 'name': 'Monthly'},
            {'id': 2, 'name': 'Quarterly'},
            {'id': 3, 'name': 'Semi-Annually'},
            {'id': 4, 'name': 'Annually'},
            {'id': 5, 'name': 'Other'},
        ]
    
    @staticmethod
    def contract_payment_terms():
        return [
            {'id': 1, 'name': 'Cash'},
            {'id': 2, 'name': 'Check'},
            {'id': 3, 'name': 'Credit Card'},
            {'id': 4, 'name': 'Other'},
        ]
    
    @staticmethod
    def lead_types():
        return [
            {'id': 1, 'name': 'Prospect'},
            {'id': 2, 'name': 'Customer'},
            {'id': 3, 'name': 'Other'},
            {'id': 4, 'name': 'Converted'},
        ]

    @staticmethod    
    def lead_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Assigned'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Converted'},
            {'id': 5, 'name': 'Closed'},
            {'id': 6, 'name': 'Deleted'},
        ]

    @staticmethod
    def document_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Draft'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Active'},
            {'id': 5, 'name': 'Closed'},
            {'id': 6, 'name': 'Deleted'},
        ]

    @staticmethod
    def quote_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Assigned'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Converted'},
            {'id': 5, 'name': 'Closed'},
            {'id': 6, 'name': 'Deleted'},
        ]

    @staticmethod
    def lead_sources():
        return [
            {'id': 1, 'name': 'Cold Call'},
            {'id': 2, 'name': 'Existing Customer'},
            {'id': 3, 'name': 'Self Generated'},
            {'id': 4, 'name': 'Employee'},
            {'id': 5, 'name': 'Partner'},
            {'id': 6, 'name': 'Public Relations'},
            {'id': 7, 'name': 'Direct Mail'},
            {'id': 8, 'name': 'Conference'},
            {'id': 9, 'name': 'Trade Show'},
            {'id': 10, 'name': 'Web Site'},
            {'id': 11, 'name': 'Word of Mouth'},
            {'id': 12, 'name': 'Email'},
            {'id': 13, 'name': 'Campaign'},
            {'id': 14, 'name': 'Other'},
        ]

    @staticmethod
    def lead_priorities():
        return [
            {'id': 1, 'name': 'Low'},
            {'id': 2, 'name': 'Medium'},
            {'id': 3, 'name': 'High'},
            {'id': 4, 'name': 'Urgent'},
        ]

    @staticmethod
    def task_priorities():
        return [
            {'id': 1, 'name': 'Low'},
            {'id': 2, 'name': 'Medium'},
            {'id': 3, 'name': 'High'},
            {'id': 4, 'name': 'Urgent'},
        ]

    @staticmethod
    def group_types():
        return [
            {'id': 1, 'name': 'Sales'},
            {'id': 2, 'name': 'Marketing'},
            {'id': 3, 'name': 'Admin'},
        ]

    @staticmethod
    def opportunity_types():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Existing'},
            {'id': 3, 'name': 'Other'},
        ]

    @staticmethod
    def opportunity_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Assigned'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Closed'},
            {'id': 5, 'name': 'Deleted'},
        ]

    @staticmethod
    def campaign_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Assigned'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Closed'},
            {'id': 5, 'name': 'Deleted'},
        ]

    @staticmethod
    def case_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Assigned'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Closed'},
            {'id': 5, 'name': 'Deleted'},
        ]
    
    @staticmethod
    def task_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Assigned'},
            {'id': 3, 'name': 'In Progress'},
            {'id': 4, 'name': 'Closed'},
            {'id': 5, 'name': 'Deleted'},
        ]

    @staticmethod
    def task_types():
        return [
            {'id': 1, 'name': 'User'},
            {'id': 2, 'name': 'System'},
        ]

    @staticmethod
    def campaign_types():
        return [
            {'id': 1, 'name': 'Email'},
            {'id': 2, 'name': 'Facebook'},
            {'id': 3, 'name': 'Adwords'},
            {'id': 4, 'name': 'Web'},
            {'id': 5, 'name': 'Mail'},
            {'id': 6, 'name': 'Print'},
            {'id': 7, 'name': 'Other'},
        ]

    @staticmethod
    def opportunity_priorities():
        return [
            {'id': 1, 'name': 'Low'},
            {'id': 2, 'name': 'Medium'},
            {'id': 3, 'name': 'High'},
            {'id': 4, 'name': 'Urgent'},
        ]

    @staticmethod
    def project_priorities():
        return [
            {'id': 1, 'name': 'Low'},
            {'id': 2, 'name': 'Medium'},
            {'id': 3, 'name': 'High'},
            {'id': 4, 'name': 'Urgent'},
        ]

    @staticmethod
    def case_priorities():
        return [
            {'id': 1, 'name': 'Low'},
            {'id': 2, 'name': 'Medium'},
            {'id': 3, 'name': 'High'},
            {'id': 4, 'name': 'Urgent'},
        ]
    
    @staticmethod
    def invoice_status():
        return [
            {'id': 1, 'name': 'New'},
            {'id': 2, 'name': 'Paid'},
            {'id': 3, 'name': 'Partially Paid'},
            {'id': 4, 'name': 'Overdue'},
            {'id': 5, 'name': 'Cancelled'},
        ]

    @staticmethod
    def meeting_status():
        return [
            {'id': 1, 'name': 'Planned'},
            {'id': 2, 'name': 'Held'},
            {'id': 3, 'name': 'Cancelled'},
        ]
    
    @staticmethod
    def meeting_types():
        return [
            {'id': 1, 'name': 'General'},
            {'id': 2, 'name': 'Sales'},
            {'id': 3, 'name': 'Support'},
            {'id': 4, 'name': 'Other'},
        ]

    @staticmethod
    def case_types():
        return [
            {'id': 1, 'name': 'General'},
            {'id': 2, 'name': 'Sales'},
            {'id': 3, 'name': 'Support'},
            {'id': 4, 'name': 'Other'},
        ]

    @staticmethod
    def discount_types():
        return [
            {'id': 1, 'name': 'Percentage'},
            {'id': 2, 'name': 'Amount'},
        ]

    @staticmethod
    def countries():
        return [
            {'code': 'US', 'name': 'Canada'},
            {'code': 'AF', 'name': 'Afghanistan'},
            {'code': 'AL', 'name': 'Albania'},
            {'code': 'DZ', 'name': 'Algeria'},
            {'code': 'AS', 'name': 'American Samoa'},
            {'code': 'AD', 'name': 'Andorra'},
            {'code': 'AO', 'name': 'Angola'},
            {'code': 'AI', 'name': 'Anguilla'},
            {'code': 'AQ', 'name': 'Antarctica'},
            {'code': 'AG', 'name': 'Antigua and/or Barbuda'},
            {'code': 'AR', 'name': 'Argentina'},
            {'code': 'AM', 'name': 'Armenia'},
            {'code': 'AW', 'name': 'Aruba'},
            {'code': 'AU', 'name': 'Australia'},
            {'code': 'AT', 'name': 'Austria'},
            {'code': 'AZ', 'name': 'Azerbaijan'},
            {'code': 'BS', 'name': 'Bahamas'},
            {'code': 'BH', 'name': 'Bahrain'},
            {'code': 'BD', 'name': 'Bangladesh'},
            {'code': 'BB', 'name': 'Barbados'},
            {'code': 'BY', 'name': 'Belarus'},
            {'code': 'BE', 'name': 'Belgium'},
            {'code': 'BZ', 'name': 'Belize'},
            {'code': 'BJ', 'name': 'Benin'},
            {'code': 'BM', 'name': 'Bermuda'},
            {'code': 'BT', 'name': 'Bhutan'},
            {'code': 'BO', 'name': 'Bolivia'},
            {'code': 'BA', 'name': 'Bosnia and Herzegovina'},
            {'code': 'BW', 'name': 'Botswana'},
            {'code': 'BV', 'name': 'Bouvet Island'},
            {'code': 'BR', 'name': 'Brazil'},
            {'code': 'IO', 'name': 'British Indian Ocean Territory'},
            {'code': 'BN', 'name': 'Brunei Darussalam'},
            {'code': 'BG', 'name': 'Bulgaria'},
            {'code': 'BF', 'name': 'Burkina Faso'},
            {'code': 'BI', 'name': 'Burundi'},
            {'code': 'KH', 'name': 'Cambodia'},
            {'code': 'CM', 'name': 'Cameroon'},
            {'code': 'CV', 'name': 'Cape Verde'},
            {'code': 'KY', 'name': 'Cayman Islands'},
            {'code': 'CF', 'name': 'Central African Republic'},
            {'code': 'TD', 'name': 'Chad'},
            {'code': 'CL', 'name': 'Chile'},
            {'code': 'CN', 'name': 'China'},
            {'code': 'CX', 'name': 'Christmas Island'},
            {'code': 'CC', 'name': 'Cocos (Keeling) Islands'},
            {'code': 'CO', 'name': 'Colombia'},
            {'code': 'KM', 'name': 'Comoros'},
            {'code': 'CG', 'name': 'Congo'},
            {'code': 'CK', 'name': 'Cook Islands'},
            {'code': 'CR', 'name': 'Costa Rica'},
            {'code': 'HR', 'name': 'Croatia (Hrvatska)'},
            {'code': 'CU', 'name': 'Cuba'},
            {'code': 'CY', 'name': 'Cyprus'},
            {'code': 'CZ', 'name': 'Czech Republic'},
            {'code': 'DK', 'name': 'Denmark'},
            {'code': 'DJ', 'name': 'Djibouti'},
            {'code': 'DM', 'name': 'Dominica'},
            {'code': 'DO', 'name': 'Dominican Republic'},
            {'code': 'TP', 'name': 'East Timor'},
            {'code': 'EC', 'name': 'Ecuador'},
            {'code': 'EG', 'name': 'Egypt'},
            {'code': 'SV', 'name': 'El Salvador'},
            {'code': 'GQ', 'name': 'Equatorial Guinea'},
            {'code': 'ER', 'name': 'Eritrea'},
            {'code': 'EE', 'name': 'Estonia'},
            {'code': 'ET', 'name': 'Ethiopia'},
            {'code': 'FK', 'name': 'Falkland Islands (Malvinas)'},
            {'code': 'FO', 'name': 'Faroe Islands'},
            {'code': 'FJ', 'name': 'Fiji'},
            {'code': 'FI', 'name': 'Finland'},
            {'code': 'FR', 'name': 'France'},
            {'code': 'FX', 'name': 'France, Metropolitan'},
            {'code': 'GF', 'name': 'French Guiana'},
            {'code': 'PF', 'name': 'French Polynesia'},
            {'code': 'TF', 'name': 'French Southern Territories'},
            {'code': 'GA', 'name': 'Gabon'},
            {'code': 'GM', 'name': 'Gambia'},
            {'code': 'GE', 'name': 'Georgia'},
            {'code': 'DE', 'name': 'Germany'},
            {'code': 'GH', 'name': 'Ghana'},
            {'code': 'GI', 'name': 'Gibraltar'},
            {'code': 'GR', 'name': 'Greece'},
            {'code': 'GL', 'name': 'Greenland'},
            {'code': 'GD', 'name': 'Grenada'},
            {'code': 'GP', 'name': 'Guadeloupe'},
            {'code': 'GU', 'name': 'Guam'},
            {'code': 'GT', 'name': 'Guatemala'},
            {'code': 'GN', 'name': 'Guinea'},
            {'code': 'GW', 'name': 'Guinea-Bissau'},
            {'code': 'GY', 'name': 'Guyana'},
            {'code': 'HT', 'name': 'Haiti'},
            {'code': 'HM', 'name': 'Heard and Mc Donald Islands'},
            {'code': 'HN', 'name': 'Honduras'},
            {'code': 'HK', 'name': 'Hong Kong'},
            {'code': 'HU', 'name': 'Hungary'},
            {'code': 'IS', 'name': 'Iceland'},
            {'code': 'IN', 'name': 'India'},
            {'code': 'ID', 'name': 'Indonesia'},
            {'code': 'IR', 'name': 'Iran (Islamic Republic of)'},
            {'code': 'IQ', 'name': 'Iraq'},
            {'code': 'IE', 'name': 'Ireland'},
            {'code': 'IL', 'name': 'Israel'},
            {'code': 'IT', 'name': 'Italy'},
            {'code': 'CI', 'name': 'Ivory Coast'},
            {'code': 'JM', 'name': 'Jamaica'},
            {'code': 'JP', 'name': 'Japan'},
            {'code': 'JO', 'name': 'Jordan'},
            {'code': 'KZ', 'name': 'Kazakhstan'},
            {'code': 'KE', 'name': 'Kenya'},
            {'code': 'KI', 'name': 'Kiribati'},
            {'code': 'KP', 'name': 'Korea, Democratic People\'s Republic of'},
            {'code': 'KR', 'name': 'Korea, Republic of'},
            {'code': 'KW', 'name': 'Kuwait'},
            {'code': 'KG', 'name': 'Kyrgyzstan'},
            {'code': 'LA', 'name': 'Lao People\'s Democratic Republic'},
            {'code': 'LV', 'name': 'Latvia'},
            {'code': 'LB', 'name': 'Lebanon'},
            {'code': 'LS', 'name': 'Lesotho'},
            {'code': 'LR', 'name': 'Liberia'},
            {'code': 'LY', 'name': 'Libyan Arab Jamahiriya'},
            {'code': 'LI', 'name': 'Liechtenstein'},
            {'code': 'LT', 'name': 'Lithuania'},
            {'code': 'LU', 'name': 'Luxembourg'},
            {'code': 'MO', 'name': 'Macau'},
            {'code': 'MK', 'name': 'Macedonia'},
            {'code': 'MG', 'name': 'Madagascar'},
            {'code': 'MW', 'name': 'Malawi'},
            {'code': 'MY', 'name': 'Malaysia'},
            {'code': 'MV', 'name': 'Maldives'},
            {'code': 'ML', 'name': 'Mali'},
            {'code': 'MT', 'name': 'Malta'},
            {'code': 'MH', 'name': 'Marshall Islands'},
            {'code': 'MQ', 'name': 'Martinique'},
            {'code': 'MR', 'name': 'Mauritania'},
            {'code': 'MU', 'name': 'Mauritius'},
            {'code': 'TY', 'name': 'Mayotte'},
            {'code': 'MX', 'name': 'Mexico'},
            {'code': 'FM', 'name': 'Micronesia, Federated States of'},
            {'code': 'MD', 'name': 'Moldova, Republic of'},
            {'code': 'MC', 'name': 'Monaco'},
            {'code': 'MN', 'name': 'Mongolia'},
            {'code': 'MS', 'name': 'Montserrat'},
            {'code': 'MA', 'name': 'Morocco'},
            {'code': 'MZ', 'name': 'Mozambique'},
            {'code': 'MM', 'name': 'Myanmar'},
            {'code': 'NA', 'name': 'Namibia'},
            {'code': 'NR', 'name': 'Nauru'},
            {'code': 'NP', 'name': 'Nepal'},
            {'code': 'NL', 'name': 'Netherlands'},
            {'code': 'AN', 'name': 'Netherlands Antilles'},
            {'code': 'NC', 'name': 'New Caledonia'},
            {'code': 'NZ', 'name': 'New Zealand'},
            {'code': 'NI', 'name': 'Nicaragua'},
            {'code': 'NE', 'name': 'Niger'},
            {'code': 'NG', 'name': 'Nigeria'},
            {'code': 'NU', 'name': 'Niue'},
            {'code': 'NF', 'name': 'Norfork Island'},
            {'code': 'MP', 'name': 'Northern Mariana Islands'},
            {'code': 'NO', 'name': 'Norway'},
            {'code': 'OM', 'name': 'Oman'},
            {'code': 'PK', 'name': 'Pakistan'},
            {'code': 'PW', 'name': 'Palau'},
            {'code': 'PA', 'name': 'Panama'},
            {'code': 'PG', 'name': 'Papua New Guinea'},
            {'code': 'PY', 'name': 'Paraguay'},
            {'code': 'PE', 'name': 'Peru'},
            {'code': 'PH', 'name': 'Philippines'},
            {'code': 'PN', 'name': 'Pitcairn'},
            {'code': 'PL', 'name': 'Poland'},
            {'code': 'PT', 'name': 'Portugal'},
            {'code': 'PR', 'name': 'Puerto Rico'},
            {'code': 'QA', 'name': 'Qatar'},
            {'code': 'RE', 'name': 'Reunion'},
            {'code': 'RO', 'name': 'Romania'},
            {'code': 'RU', 'name': 'Russian Federation'},
            {'code': 'RW', 'name': 'Rwanda'},
            {'code': 'KN', 'name': 'Saint Kitts and Nevis'},
            {'code': 'LC', 'name': 'Saint Lucia'},
            {'code': 'VC', 'name': 'Saint Vincent and the Grenadines'},
            {'code': 'WS', 'name': 'Samoa'},
            {'code': 'SM', 'name': 'San Marino'},
            {'code': 'ST', 'name': 'Sao Tome and Principe'},
            {'code': 'SA', 'name': 'Saudi Arabia'},
            {'code': 'SN', 'name': 'Senegal'},
            {'code': 'RS', 'name': 'Serbia'},
            {'code': 'SC', 'name': 'Seychelles'},
            {'code': 'SL', 'name': 'Sierra Leone'},
            {'code': 'SG', 'name': 'Singapore'},
            {'code': 'SK', 'name': 'Slovakia'},
            {'code': 'SI', 'name': 'Slovenia'},
            {'code': 'SB', 'name': 'Solomon Islands'},
            {'code': 'SO', 'name': 'Somalia'},
            {'code': 'ZA', 'name': 'South Africa'},
            {'code': 'GS', 'name': 'South Georgia South Sandwich Islands'},
            {'code': 'ES', 'name': 'Spain'},
            {'code': 'LK', 'name': 'Sri Lanka'},
            {'code': 'SH', 'name': 'St. Helena'},
            {'code': 'PM', 'name': 'St. Pierre and Miquelon'},
            {'code': 'SD', 'name': 'Sudan'},
            {'code': 'SR', 'name': 'Suriname'},
            {'code': 'SJ', 'name': 'Svalbarn and Jan Mayen Islands'},
            {'code': 'SZ', 'name': 'Swaziland'},
            {'code': 'SE', 'name': 'Sweden'},
            {'code': 'CH', 'name': 'Switzerland'},
            {'code': 'SY', 'name': 'Syrian Arab Republic'},
            {'code': 'TW', 'name': 'Taiwan'},
            {'code': 'TJ', 'name': 'Tajikistan'},
            {'code': 'TZ', 'name': 'Tanzania, United Republic of'},
            {'code': 'TH', 'name': 'Thailand'},
            {'code': 'TG', 'name': 'Togo'},
            {'code': 'TK', 'name': 'Tokelau'},
            {'code': 'TO', 'name': 'Tonga'},
            {'code': 'TT', 'name': 'Trinidad and Tobago'},
            {'code': 'TN', 'name': 'Tunisia'},
            {'code': 'TR', 'name': 'Turkey'},
            {'code': 'TM', 'name': 'Turkmenistan'},
            {'code': 'TC', 'name': 'Turks and Caicos Islands'},
            {'code': 'TV', 'name': 'Tuvalu'},
            {'code': 'UG', 'name': 'Uganda'},
            {'code': 'UA', 'name': 'Ukraine'},
            {'code': 'AE', 'name': 'United Arab Emirates'},
            {'code': 'GB', 'name': 'United Kingdom'},
            {'code': 'CA', 'name': 'United States'},
            {'code': 'UM', 'name': 'United States minor outlying islands'},
            {'code': 'UY', 'name': 'Uruguay'},
            {'code': 'UZ', 'name': 'Uzbekistan'},
            {'code': 'VU', 'name': 'Vanuatu'},
            {'code': 'VA', 'name': 'Vatican City State'},
            {'code': 'VE', 'name': 'Venezuela'},
            {'code': 'VN', 'name': 'Vietnam'},
            {'code': 'VG', 'name': 'Virgin Islands (British)'},
            {'code': 'VI', 'name': 'Virgin Islands (U.S.)'},
            {'code': 'WF', 'name': 'Wallis and Futuna Islands'},
            {'code': 'EH', 'name': 'Western Sahara'},
            {'code': 'YE', 'name': 'Yemen'},
            {'code': 'YU', 'name': 'Yugoslavia'},
            {'code': 'ZR', 'name': 'Zaire'},
            {'code': 'ZM', 'name': 'Zambia'},
            {'code': 'ZW', 'name': 'Zimbabwe'}
        ]

    @staticmethod
    def states():
        return [
            # Canada
            {'code': 'CA', 'abbreviation': 'AB', 'name': 'Alberta'},
            {'code': 'CA', 'abbreviation': 'BC', 'name': 'British Columbia'},
            {'code': 'CA', 'abbreviation': 'MB', 'name': 'Manitoba'},
            {'code': 'CA', 'abbreviation': 'NB', 'name': 'New Brunswick'},
            {'code': 'CA', 'abbreviation': 'NL', 'name': 'Newfoundland and Labrador'},
            {'code': 'CA', 'abbreviation': 'NT', 'name': 'Northwest Territories'},
            {'code': 'CA', 'abbreviation': 'NS', 'name': 'Nova Scotia'},
            {'code': 'CA', 'abbreviation': 'NU', 'name': 'Nunavut'},
            {'code': 'CA', 'abbreviation': 'ON', 'name': 'Ontario'},
            {'code': 'CA', 'abbreviation': 'PE', 'name': 'Prince Edward Island'},
            {'code': 'CA', 'abbreviation': 'QC', 'name': 'Quebec'},
            {'code': 'CA', 'abbreviation': 'SK', 'name': 'Saskatchewan'},
            {'code': 'CA', 'abbreviation': 'YT', 'name': 'Yukon'},

            # USA
            {'code': 'US', 'abbreviation': 'AL', 'name': 'Alabama'},
            {'code': 'US', 'abbreviation': 'AK', 'name': 'Alaska'},
            {'code': 'US', 'abbreviation': 'AZ', 'name': 'Arizona'},
            {'code': 'US', 'abbreviation': 'AR', 'name': 'Arkansas'},
            {'code': 'US', 'abbreviation': 'CA', 'name': 'California'},
            {'code': 'US', 'abbreviation': 'CO', 'name': 'Colorado'},
            {'code': 'US', 'abbreviation': 'CT', 'name': 'Connecticut'},
            {'code': 'US', 'abbreviation': 'DE', 'name': 'Delaware'},
            {'code': 'US', 'abbreviation': 'FL', 'name': 'Florida'},
            {'code': 'US', 'abbreviation': 'GA', 'name': 'Georgia'},
            {'code': 'US', 'abbreviation': 'HI', 'name': 'Hawaii'},
            {'code': 'US', 'abbreviation': 'ID', 'name': 'Idaho'},
            {'code': 'US', 'abbreviation': 'IL', 'name': 'Illinois'},
            {'code': 'US', 'abbreviation': 'IN', 'name': 'Indiana'},
            {'code': 'US', 'abbreviation': 'IA', 'name': 'Iowa'},
            {'code': 'US', 'abbreviation': 'KS', 'name': 'Kansas'},
            {'code': 'US', 'abbreviation': 'KY', 'name': 'Kentucky'},
            {'code': 'US', 'abbreviation': 'LA', 'name': 'Louisiana'},
            {'code': 'US', 'abbreviation': 'ME', 'name': 'Maine'},
            {'code': 'US', 'abbreviation': 'MD', 'name': 'Maryland'},
            {'code': 'US', 'abbreviation': 'MA', 'name': 'Massachusetts'},
            {'code': 'US', 'abbreviation': 'MI', 'name': 'Michigan'},
            {'code': 'US', 'abbreviation': 'MN', 'name': 'Minnesota'},
            {'code': 'US', 'abbreviation': 'MS', 'name': 'Mississippi'},
            {'code': 'US', 'abbreviation': 'MO', 'name': 'Missouri'},
            {'code': 'US', 'abbreviation': 'MT', 'name': 'Montana'},
            {'code': 'US', 'abbreviation': 'NE', 'name': 'Nebraska'},
            {'code': 'US', 'abbreviation': 'NV', 'name': 'Nevada'},
            {'code': 'US', 'abbreviation': 'NH', 'name': 'New Hampshire'},
            {'code': 'US', 'abbreviation': 'NJ', 'name': 'New Jersey'},
            {'code': 'US', 'abbreviation': 'NM', 'name': 'New Mexico'},
            {'code': 'US', 'abbreviation': 'NY', 'name': 'New York'},
            {'code': 'US', 'abbreviation': 'NC', 'name': 'North Carolina'},
            {'code': 'US', 'abbreviation': 'ND', 'name': 'North Dakota'},
            {'code': 'US', 'abbreviation': 'OH', 'name': 'Ohio'},
            {'code': 'US', 'abbreviation': 'OK', 'name': 'Oklahoma'},
            {'code': 'US', 'abbreviation': 'OR', 'name': 'Oregon'},
            {'code': 'US', 'abbreviation': 'PA', 'name': 'Pennsylvania'},
            {'code': 'US', 'abbreviation': 'RI', 'name': 'Rhode Island'},
            {'code': 'US', 'abbreviation': 'SC', 'name': 'South Carolina'},
            {'code': 'US', 'abbreviation': 'SD', 'name': 'South Dakota'},
            {'code': 'US', 'abbreviation': 'TN', 'name': 'Tennessee'},
            {'code': 'US', 'abbreviation': 'TX', 'name': 'Texas'},
            {'code': 'US', 'abbreviation': 'UT', 'name': 'Utah'},
            {'code': 'US', 'abbreviation': 'VT', 'name': 'Vermont'},
            {'code': 'US', 'abbreviation': 'VA', 'name': 'Virginia'},
            {'code': 'US', 'abbreviation': 'WA', 'name': 'Washington'},
            {'code': 'US', 'abbreviation': 'WV', 'name': 'West Virginia'},
            {'code': 'US', 'abbreviation': 'WI', 'name': 'Wisconsin'},
            {'code': 'US', 'abbreviation': 'WY', 'name': 'Wyoming'},
            {'code': 'US', 'abbreviation': 'AS', 'name': 'American Samoa'},
            {'code': 'US', 'abbreviation': 'DC', 'name': 'District of Columbia'},
            {'code': 'US', 'abbreviation': 'GU', 'name': 'Guam'},
            {'code': 'US', 'abbreviation': 'MP', 'name': 'Northern Mariana Islands'},
            {'code': 'US', 'abbreviation': 'PR', 'name': 'Puerto Rico'},
            {'code': 'US', 'abbreviation': 'VI', 'name': 'United States Virgin Islands'},
        ]

    @staticmethod
    def input_type():
        return [
            {'name': 'tel', 'mask': ''},
            {'name': 'email', 'mask': ''},
            {'name': 'city', 'mask': ''},
            {'name': 'custom', 'mask': ''},
            {'name': 'checkbox', 'mask': ''},
            {'name': 'color', 'mask': ''},
            {'name': 'date', 'mask': ''},
            {'name': 'datetime-local', 'mask': ''},
            {'name': 'file', 'mask': ''},
            {'name': 'hidden', 'mask': ''},
            {'name': 'image', 'mask': ''},
            {'name': 'map', 'mask': ''},
            {'name': 'month', 'mask': ''},
            {'name': 'number', 'mask': ''},
            {'name': 'password', 'mask': ''},
            {'name': 'radio', 'mask': ''},
            {'name': 'range', 'mask': ''},
            {'name': 'select', 'mask': ''},
            {'name': 'select_mulitple', 'mask': ''},
            {'name': 'text', 'mask': ''},
            {'name': 'time', 'mask': ''},
            {'name': 'url', 'mask': ''},
            {'name': 'week', 'mask': ''},
            {'name': 'textarea', 'mask': ''},
            {'name': 'video', 'mask': ''},
            {'name': 'zip', 'mask': ''},
            {'name': 'address', 'mask': ''},
            {'name': 'related', 'mask': ''}
        ]
