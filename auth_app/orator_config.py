from orator import DatabaseManager, Model
from decouple import config

def setup_orator():
    db_config = {
        'mysql': {
            'driver': 'mysql',
            'host': config('DATABASE_HOST'),
            'database': config('DATABASE_NAME'),
            'user': config('DATABASE_USER'),
            'password': config('DATABASE_PASSWORD'),
            'prefix': ''
        }
    }

    db = DatabaseManager(db_config)
    Model.set_connection_resolver(db)
    return db

db = setup_orator()