import logging
from orator.seeds import Seeder
from .module_seeder import ModuleSeeder
from .field_seeder import FieldSeeder
from .relationship_seeder import RelationshipSeeder
from .generate_seeder import GenerateSeeder
from .module_subpanel_seeder import ModuleSubpanelSeeder

class DatabaseSeeder(Seeder):

    def run(self):
        logging.basicConfig(level=logging.INFO)
        logging.info('Start Seeding')

        print ("call module")
        self.call(ModuleSeeder)
        print ("call field")
        self.call(FieldSeeder)
        print ("call relationship")
        self.call(RelationshipSeeder)
        self.call(GenerateSeeder)
        self.call(ModuleSubpanelSeeder)

        logging.info('Complete')
