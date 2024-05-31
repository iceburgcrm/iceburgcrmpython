from orator import Model, DatabaseManager
from auth_app.orator_config import db

class Setting(Model):
    __table__ = 'ice_settings'

    @staticmethod
    def get_setting(key):
        setting = Setting.where('name', key).first()
        if setting:
            value = setting.value
        else:
            value = None 
        if not value and key == 'theme':
            return 'light'
        return value

    @staticmethod
    def get_themes():
        return db.table('ice_themes').get()

    @staticmethod
    def get_settings(request):
        data = {}
        for item in Setting.all():
            data[item.name] = item.value
        if not request.user.is_authenticated:
             logo_setting = Setting.where('name', 'logo').first()
             if logo_setting:
                logo = logo_setting.additional_data
                if logo:
                    data['logo'] = logo
        return data

    @staticmethod
    def get_breadcrumbs(level1=None, level2=None, level3=None):
        data = [{'name': 'Home', 'url': '/dashboard', 'svg': 'home'}]
        if level1:
            data.append(level1)
        if level2:
            data.append(level2)
        if level3:
            data.append(level3)
        return data

    @staticmethod
    def save_settings(settings):
        for key, value in settings.items():
            Setting.where('name', key).update({'value': value})
        return 1

