from django.core.management.base import BaseCommand
from orator import DatabaseManager, Model
from orator.orm import Factory
from orator.seeds import Seeder
from orator.orm import has_many, has_one, belongs_to
from datetime import datetime
import json
from auth_app.orator_config import db
from seeders.database_seeders import DatabaseSeeder
from orator import Schema
from seeders.core_seeder import CoreSeeder

class Command(BaseCommand):
    help = 'Seed database using Orator seeder'

    def handle(self, *args, **options):
        

        CoreSeeder.migration()
        Model.set_connection_resolver(db)

        seeder = Seeder(db)
        seeder.call(DatabaseSeeder)  
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database.'))