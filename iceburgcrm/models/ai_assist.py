import os
from openai import OpenAI


from orator import Model
from .field import Field

class AIAssist(Model):
    __table__ = 'ai_assists'
    client = None
    def __init__():
        pass
        

    @staticmethod
    def suggest_fields(module_id, data, additional_text=""):
        module = AIAssist.where('id', module_id).first()
        txt = f"Complete the following values for the fields below. They are from a CRM module called {module.name}."
        txt += "\n\n Return an Array with the field name (exactly as given) and the completed value."
        txt += " Follow the rules for each array item and reset the rules for each item. Only return the data as json."
        txt += " Only return the name and value field. Do not include comments only the array. TRY TO BE CREATIVE IN YOUR ANSWERS."

        for key, value in data['ai_fields'].items():
            if value:
                field = Field.where('name', key).first()
                if field:
                    rules = f"Datatype is: {field.data_type}. Input type is: {field.input_type}."
                    rules += f" Maximum Field Length is: {field.field_length}."
                    rules += f" Data must be a base64 encoded image." if field.input_type == 'image' else ""
                    rules += f" Must have {field.decimal_places} decimal places." if field.decimal_places else ""
                    txt += f"   {{'name': key, 'value': data['field_data'].get(f'1__{key}', ''), 'rules': rules}}"

        txt += additional_text
        response = AIAssist.get_data(txt)
        return response

    @staticmethod
    def get_data(content):
        response = client.chat.completions.create(model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': content}])
        return response.choices[0].message.content


