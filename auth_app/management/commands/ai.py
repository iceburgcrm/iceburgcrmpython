from django.core.management.base import BaseCommand
from orator import DatabaseManager, Model
from orator.orm import Factory
from orator.seeds import Seeder
from orator.orm import has_many, has_one, belongs_to
from datetime import datetime
import json
from auth_app.orator_config import db
from iceburgcrm.models.module import Module
from seeders.database_seeders import DatabaseSeeder
from iceburgcrm.models.ai_create import AICreate
from seeders.core_seeder import CoreSeeder


class Command(BaseCommand):
    help = 'AI Seed database'

    def add_arguments(self, parser):
        parser.add_argument('prompt', type=str, help='The prompt used to describe your CRM')
        parser.add_argument('--model', type=str, default='gpt-3.5-turbo', help='The model to use')
        parser.add_argument('--logo', type=bool, default=False, help='Include logo')
        parser.add_argument('--seed_amount', type=int, default=0, help='Seed amount')
        parser.add_argument('--seed_type', type=str, default='', help='Seed type')

    def handle(self, *args, **kwargs):
        prompt = kwargs['prompt']
        model = kwargs['model']
        logo = kwargs['logo']
        seed_amount = kwargs['seed_amount']
        seed_type = kwargs['seed_type']
    
        CoreSeeder.migration()
        CoreSeeder.module()
        CoreSeeder.field()
        CoreSeeder.generate()
        CoreSeeder.ai_module_seeder()

        AICreate.process(prompt, model, logo, seed_amount, seed_type)


        CoreSeeder.ai_generate_seeder()


      

        


