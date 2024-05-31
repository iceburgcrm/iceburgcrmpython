from orator import Model, Schema
from orator.orm import has_many
from datetime import datetime
from auth_app.orator_config import db
from iceburgcrm.models.relationship_module import RelationshipModule

class Relationship(Model):
    __table__ = 'ice_relationships'
    __guarded__ = []

    @has_many('relationship_id', 'id')
    def relationship_module(self):
        from .relationship_module import RelationshipModule
        return RelationshipModule

    @staticmethod
    def get_record(relationship_id=None, id=None):
        relationship = Relationship.find(relationship_id)
        return db.table(relationship.name).where('id', id).first()

    @staticmethod
    def save_record(relationship_id, records={}, record_id=0):
        from .module import Module
        relationship = Relationship.find(relationship_id)
        if not relationship:
            raise ValueError("Relationship not found")

        data = {}
        for key, value in records.items():
            module = Module.find(key)
            if module:
                data[f'{module.name}_id'] = value
            else:
                raise ValueError(f"Module with id {key} not found")

        if record_id:
            existing = db.table(relationship.name).where('id', record_id).first()
            if existing:
                db.table(relationship.name).where('id', record_id).update(data)
            else:
                data['id'] = record_id
                db.table(relationship.name).insert(data)
        else:
            db.table(relationship.name).insert(data)
        return data


    @staticmethod
    def update_or_insert(modules, relationship=None):
        from .module import Module
        module_names = []
        related_field_types = ['integer'] * len(modules)  # Presuming all related fields are integers

        for module_id in modules:
            module = Module.find(module_id)
            if module:
                module_names.append(module.name.upper())
            else:
                raise ValueError(f"Module with id {module_id} not found")

        module_name = '_'.join(module_names)

        if not relationship:
            relationship = Relationship.create(name=module_name, modules=','.join(map(str, modules)),
                                            related_field_types=','.join(related_field_types), status=1)
        else:
            relationship.name = module_name
            relationship.modules = ','.join(map(str, modules))
            relationship.related_field_types = ','.join(related_field_types)
            relationship.status = 1
            relationship.save()

        for module_id in modules:
            RelationshipModule.first_or_create(relationship_id=relationship.id, module_id=module_id)

        return relationship

    @staticmethod
    def delete_records(relationship_id, data):
        relationship = Relationship.find_or_fail(relationship_id)
        return db.table(relationship.name).where_in('id', data).delete()

    @classmethod
    def generate(self, seed=0):
        from .module import Module
        relationships = Relationship.all()

        for relationship in relationships:
            modules = relationship.modules.split(',')

            db.statement(f"DROP TABLE IF EXISTS `{relationship.name}`")

            create_table_query = f"""
                CREATE TABLE `{relationship.name}` (
                    `id` INT AUTO_INCREMENT PRIMARY KEY,
                    `status` INT DEFAULT 1,
                    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """

            for module_id in modules:
                module = Module.find(module_id)
                if module:
                    create_table_query += f", `{module.name}_id` INT UNSIGNED"

            create_table_query += ") ENGINE=InnoDB"
            db.statement(create_table_query)

            if seed > 0:
                Relationship.seed_data(relationship, seed)

        Relationship.generate_relationship_modules()

    def generate_relationship_modules():
        RelationshipModule.truncate()

        relationships = Relationship.all()
        schema = Schema(db)  

        for relationship in relationships:
            models = relationship.modules.split(',')
            for model_id in models:
                if schema.has_table(relationship.name):
                    relationship_module = RelationshipModule.where('relationship_id', relationship.id) \
                        .where('module_id', model_id) \
                        .first()

                    if not relationship_module:
                        RelationshipModule.insert({
                            'relationship_id': relationship.id,
                            'module_id': model_id
                        })

    @staticmethod
    def seed_data(relationship, seed):
        from .module import Module
        for _ in range(seed):
            data = {}
            modules = relationship.modules.split(',')
            for module_id in modules:
                module = Module.find(module_id)
                data[f'{module.name}_id'] = 1 
            db.table(relationship.name).insert(data)
