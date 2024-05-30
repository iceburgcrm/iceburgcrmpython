from orator import DatabaseManager, Model

def setup_orator():
    db_config = {
        'mysql': {
            'driver': 'mysql',
            'host': '132.145.101.132',
            'database': 'python',
            'user': 'clf55_rob',
            'password': 'babyu5',
            'prefix': ''
        }
    }

    db = DatabaseManager(db_config)
    Model.set_connection_resolver(db)
    return db

db = setup_orator()
