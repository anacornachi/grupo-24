try:
    import oracledb
except ImportError:
    oracledb = None

from dotenv import load_dotenv
import os

load_dotenv()
#
DB_USER = os.getenv("ORACLE_USER")
DB_PASSWORD = os.getenv("ORACLE_PASSWORD")
DB_HOST = os.getenv("ORACLE_HOST")
DB_PORT = os.getenv("ORACLE_PORT")
DB_SERVICE = os.getenv("ORACLE_SERVICE")


def get_connection():
    if oracledb is None:
        raise ImportError("A biblioteca 'oracledb' não está instalada. Instale-a para conectar ao banco de dados.")
    dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
    return oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn)
