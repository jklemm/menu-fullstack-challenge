MYSQL_PROD = {
    'engine': 'mysql+mysqldb',
    'pool_size': 100,
    'debug': False,
    'username': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'db_name': 'menu_db',
}

MYSQL_TEST = {
    'engine': 'mysql+mysqldb',
    'pool_size': 100,
    'debug': True,
    'username': 'root',
    'password': '',
    'host': 'localhost',
    'port': 3306,
    'db_name': 'test_menu_db',
}

SQLALCHEMY = {
    'debug': False,
}
