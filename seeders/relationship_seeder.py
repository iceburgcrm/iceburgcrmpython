from orator.seeds import Seeder
from iceburgcrm.models.relationship import Relationship
from iceburgcrm.models.module import Module
import logging

class RelationshipSeeder(Seeder):
    def run(self):
        Relationship.truncate()

        # Create relationships
        relationships = [
            {"name": "accounts_contacts", "modules": [Module.get_id("accounts"), Module.get_id("contacts")]},
            {"name": "accounts_opportunities", "modules": [Module.get_id("accounts"), Module.get_id("opportunities")]},
            {"name": "leads_accounts_opportunities", "modules": [Module.get_id("leads"), Module.get_id("accounts"), Module.get_id("opportunities")]},
            {"name": "accounts_cases", "modules": [Module.get_id("accounts"), Module.get_id("cases")]},
            {"name": "accounts_contracts", "modules": [Module.get_id("accounts"), Module.get_id("contracts")]},
            {"name": "accounts_meetings", "modules": [Module.get_id("accounts"), Module.get_id("meetings")]},
            {"name": "opportunities_contacts", "modules": [Module.get_id("opportunities"), Module.get_id("contacts")]},
            {"name": "opportunities_cases", "modules": [Module.get_id("opportunities"), Module.get_id("cases")]},
            {"name": "opportunities_contracts", "modules": [Module.get_id("opportunities"), Module.get_id("contracts")]},
            {"name": "opportunities_meetings", "modules": [Module.get_id("opportunities"), Module.get_id("meetings")]},
            {"name": "user_meetings", "modules": [Module.get_id("ice_users"), Module.get_id("meetings")]},
            {"name": "contracts_lineitems", "modules": [Module.get_id("contracts"), Module.get_id("lineitems")]},
            {"name": "users_tasks", "modules": [Module.get_id("ice_users"), Module.get_id("tasks")]},
            {"name": "projects_tasks", "modules": [Module.get_id("projects"), Module.get_id("tasks")]},
            {"name": "campaigns_tasks", "modules": [Module.get_id("campaigns"), Module.get_id("tasks")]},
            {"name": "documents_tasks", "modules": [Module.get_id("documents"), Module.get_id("tasks")]},
            {"name": "documents_accounts", "modules": [Module.get_id("documents"), Module.get_id("accounts")]},
            {"name": "documents_opportunities", "modules": [Module.get_id("documents"), Module.get_id("opportunities")]},
            {"name": "documents_cases", "modules": [Module.get_id("documents"), Module.get_id("cases")]},
            {"name": "documents_contracts", "modules": [Module.get_id("documents"), Module.get_id("contracts")]},
            {"name": "documents_meetings", "modules": [Module.get_id("documents"), Module.get_id("meetings")]},
            {"name": "notes_accounts", "modules": [Module.get_id("notes"), Module.get_id("accounts")]},
            {"name": "notes_opportunities", "modules": [Module.get_id("notes"), Module.get_id("opportunities")]},
            {"name": "notes_cases", "modules": [Module.get_id("notes"), Module.get_id("cases")]},
            {"name": "notes_contracts", "modules": [Module.get_id("notes"), Module.get_id("contracts")]},
            {"name": "notes_meetings", "modules": [Module.get_id("notes"), Module.get_id("meetings")]},
            {"name": "notes_tasks", "modules": [Module.get_id("notes"), Module.get_id("tasks")]},
            {"name": "notes_users", "modules": [Module.get_id("notes"), Module.get_id("ice_users")]},
            {"name": "groups_accounts", "modules": [Module.get_id("groups"), Module.get_id("accounts")]},
            {"name": "projects_accounts", "modules": [Module.get_id("projects"), Module.get_id("accounts")]},
            {"name": "campaigns_accounts", "modules": [Module.get_id("campaigns"), Module.get_id("accounts")]},
            {"name": "opportunities_quotes", "modules": [Module.get_id("opportunities"), Module.get_id("quotes")]},
            {"name": "opportunities_quotes_accounts", "modules": [Module.get_id("opportunities"), Module.get_id("quotes"), Module.get_id("accounts")]},
            {"name": "accounts_invoices", "modules": [Module.get_id("accounts"), Module.get_id("invoices")]},
            {"name": "accounts_invoices_users", "modules": [Module.get_id("accounts"), Module.get_id("invoices"), Module.get_id("ice_users")]},
            {"name": "modules_fields", "modules": [Module.get_id("ice_modules"), Module.get_id("ice_fields")]},
            {"name": "modules_subpanels", "modules": [Module.get_id("ice_modules"), Module.get_id("ice_module_subpanels")]},
            {"name": "modules_datalets", "modules": [Module.get_id("ice_modules"), Module.get_id("ice_datalets")]}
        ]

        for relationship in relationships:
            Relationship.insert({
                "name": relationship["name"],
                "modules": ",".join(map(str, relationship["modules"])),
                "related_field_types": "integer,integer"
            })
        
        relationship = Relationship()
        relationship.generate(6)

        logging.info('Relationship Seeding Complete')
