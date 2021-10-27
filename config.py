class Config(object):
    SECRET_KEY='7110c8ae51ert345345aef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://ingelnwq_sa:uvAT0;p+2N*[@localhost/ingelnwq_sa'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=False
    REPO_CERTIFICADOS='/home/ingelnwq/certificados/'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:mysql@localhost/ingenia_sa'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_ECHO=True
    REPO_CERTIFICADOS='/home/apolo/aplicaciones/abcdroid/clientes/ingenia/ingenia-sa/certificados'

class TestingConfig(Config):
    TESTING = True