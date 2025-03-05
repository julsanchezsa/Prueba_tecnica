import os

# Obtenemos la ruta base del directorio actual
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuración de la base de datos con SQLite.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, '..', 'database.db')
    