from orator.seeds import Seeder
from iceburgcrm.models.log import Log
from iceburgcrm.models.module_subpanel import ModuleSubpanel
from iceburgcrm.models.module import Module
from iceburgcrm.models.relationship import Relationship
from iceburgcrm.models.subpanel_field import SubpanelField
from iceburgcrm.models.field import Field
import logging


class ModuleSubpanelSeeder(Seeder):
    def run(self):
        ModuleSubpanel.truncate()
        SubpanelField.truncate()

        relationships = Relationship.all()
        modules = Module.all()
        fields = Field.all()

        subpanel_data = [
            {
                "name": "accounts_contacts",
                "label": "Contacts",
                "relationship_name": ["accounts_contacts", "contacts_accounts"],
                "module_name": "accounts",
                "fields": ["profile_pic", "first_name", "last_name"]
            },
            {
                "name": "leads_accounts_opportunities",
                "label": "Leads and Opportunities",
                "relationship_name": "leads_accounts_opportunities",
                "module_name": "accounts",
                "fields": ["first_name", "last_name", "name"],
                "field_module_names": ["leads", "leads", "opportunities"]
            },
            {
                "name": "contacts_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_contacts", "contacts_accounts"],
                "module_name": "contacts",
                "fields": ["profile_pic"]
            },
            {
                "name": "accounts_opportunities",
                "label": "Opportunities",
                "relationship_name": ["accounts_opportunities", "opportunities_accounts"],
                "module_name": "accounts",
                "fields": ["name"],
                "field_module_names": ["opportunities"]
            },
            {
                "name": "opportunities_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_opportunities", "opportunities_accounts"],
                "module_name": "opportunities",
                "fields": ["name"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "accounts_cases",
                "label": "Cases",
                "relationship_name": ["accounts_cases", "cases_accounts"],
                "module_name": "accounts",
                "fields": ["name"],
                "field_module_names": ["cases"]
            },
            {
                "name": "cases_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_cases", "cases_accounts"],
                "module_name": "cases",
                "fields": ["name"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "accounts_meetings",
                "label": "Meetings",
                "relationship_name": ["accounts_meetings", "meetings_accounts"],
                "module_name": "accounts",
                "fields": ["name"],
                "field_module_names": ["meetings"]
            },
            {
                "name": "meetings_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_meetings", "meetings_accounts"],
                "module_name": "meetings",
                "fields": ["name"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "accounts_notes",
                "label": "Notes",
                "relationship_name": ["accounts_notes", "notes_accounts"],
                "module_name": "accounts",
                "fields": ["subject"],
                "field_module_names": ["notes"]
            },
            {
                "name": "notes_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_notes", "notes_accounts"],
                "module_name": "notes",
                "fields": ["subject"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "accounts_documents",
                "label": "Documents",
                "relationship_name": ["accounts_documents", "documents_accounts"],
                "module_name": "accounts",
                "fields": ["name"],
                "field_module_names": ["documents"]
            },
            {
                "name": "documents_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_documents", "documents_accounts"],
                "module_name": "documents",
                "fields": ["name"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "projects_accounts",
                "label": "Accounts",
                "relationship_name": ["projects_accounts", "accounts_projects"],
                "module_name": "projects",
                "fields": ["name"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "accounts_projects",
                "label": "Projects",
                "relationship_name": ["projects_accounts", "accounts_projects"],
                "module_name": "accounts",
                "fields": ["name"],
                "field_module_names": ["projects"]
            },
            {
                "name": "contracts_notes",
                "label": "Notes",
                "relationship_name": ["contracts_notes", "notes_contracts"],
                "module_name": "contracts",
                "fields": ["subject"],
                "field_module_names": ["notes"]
            },
            {
                "name": "notes_contracts",
                "label": "Contracts",
                "relationship_name": ["contracts_notes", "notes_contracts"],
                "module_name": "notes",
                "fields": ["subject"],
                "field_module_names": ["contracts"]
            },
            {
                "name": "accounts_invoices",
                "label": "Invoices",
                "relationship_name": ["accounts_invoices", "invoices_accounts"],
                "module_name": "accounts",
                "fields": ["total"],
                "field_module_names": ["invoices"]
            },
            {
                "name": "invoices_accounts",
                "label": "Accounts",
                "relationship_name": ["accounts_invoices", "invoices_accounts"],
                "module_name": "invoices",
                "fields": ["total"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "opportunities_quotes",
                "label": "Quotes",
                "relationship_name": ["opportunities_quotes", "quotes_opportunities"],
                "module_name": "opportunities",
                "fields": ["total"],
                "field_module_names": ["quotes"]
            },
            {
                "name": "groups_accounts",
                "label": "Accounts",
                "relationship_name": ["groups_accounts", "accounts_groups"],
                "module_name": "groups",
                "fields": ["name"],
                "field_module_names": ["accounts"]
            },
            {
                "name": "accounts_groups",
                "label": "Groups",
                "relationship_name": ["groups_accounts", "accounts_groups"],
                "module_name": "accounts",
                "fields": ["name"],
                "field_module_names": ["groups"]
            }
        ]

        for data in subpanel_data:
            relationship_id = next((rel.id for rel in relationships if rel.name in data["relationship_name"]), None)
            module_id = next(mod.id for mod in modules if mod.name == data["module_name"])
            subpanel_id = ModuleSubpanel.insert_get_id({
                "name": data["name"],
                "label": data["label"],
                "relationship_id": relationship_id,
                "module_id": module_id
            })

            for field_name, module_name in zip(data["fields"], data.get("field_module_names", [data["module_name"]] * len(data["fields"]))):
                field_id = next((field.id for field in fields if field.name == field_name and field.module_id == next((mod.id for mod in modules if mod.name == module_name), None)), None)
                if field_id is not None:
                    SubpanelField.insert({
                        "subpanel_id": subpanel_id,
                        "field_id": field_id
                    })



