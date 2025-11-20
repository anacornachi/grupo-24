import os
from dotenv import load_dotenv
import time
import logging

logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

try:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import sessionmaker, scoped_session
    import oracledb
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    logger.warning("SQLAlchemy ou oracledb não encontrados. O banco de dados não funcionará.")

# Configuração da conexão com o banco
ORACLE_USER = os.getenv('ORACLE_USER')
ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD')
ORACLE_HOST = os.getenv('ORACLE_HOST')
ORACLE_PORT = os.getenv('ORACLE_PORT')
ORACLE_SERVICE = os.getenv('ORACLE_SERVICE')

# String de conexão
if SQLALCHEMY_AVAILABLE:
    DATABASE_URL = f"oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}"

    # Configurações do engine
    ENGINE_CONFIG = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_timeout': 30,
        'pool_recycle': 1800,  # Recicla conexões a cada 30 minutos
        'pool_pre_ping': True,  # Verifica conexão antes de usar
        'echo': True  # Log de SQL
    }

def create_engine_with_retry(max_retries=3, retry_delay=5):
    """Cria o engine com retry logic."""
    if not SQLALCHEMY_AVAILABLE:
        return None
        
    for attempt in range(max_retries):
        try:
            logger.info(f"Tentativa {attempt + 1} de {max_retries} para criar engine")
            engine = create_engine(DATABASE_URL, **ENGINE_CONFIG)
            # Testa a conexão
            with engine.connect() as conn:
                conn.execute(text("SELECT 1 FROM DUAL"))
            logger.info("Engine criado com sucesso")
            return engine
        except Exception as e:
            logger.error(f"Erro ao criar engine (tentativa {attempt + 1}): {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Aguardando {retry_delay} segundos antes da próxima tentativa...")
                time.sleep(retry_delay)
            else:
                # Em vez de dar raise, retornamos None para não quebrar a aplicação inteira
                logger.error("Falha ao conectar ao banco de dados. Continuando sem persistência.")
                return None

# Cria o engine do SQLAlchemy
engine = create_engine_with_retry()

# Cria a sessão
if engine:
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
else:
    # Mock session class
    class MockSession:
        def __init__(self, *args, **kwargs): pass
        def query(self, *args, **kwargs): return self
        def filter_by(self, *args, **kwargs): return self
        def order_by(self, *args, **kwargs): return self
        def first(self): return None
        def all(self): return []
        def add(self, *args, **kwargs): pass
        def commit(self): pass
        def refresh(self, *args, **kwargs): pass
        def delete(self, *args, **kwargs): pass
        def execute(self, *args, **kwargs): pass
        def close(self): pass
        def remove(self): pass
    
    Session = MockSession

def get_session():
    try:
        if engine:
            session = Session()
            session.execute(text("SELECT 1 FROM DUAL"))
            return session
        else:
            return Session()
    except Exception as e:
        logger.error(f"Erro ao obter sessão: {str(e)}")
        if hasattr(Session, 'remove'):
            Session.remove()  
        raise

def close_session():
    try:
        if hasattr(Session, 'remove'):
            Session.remove()
    except Exception as e:
        logger.error(f"Erro ao fechar sessão: {str(e)}")

class DB:
    session = Session
    engine = engine

db = DB()
