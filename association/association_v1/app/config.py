class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://association:association@localhost/association_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'de5845838021615d5095bda09dc5613ae0931788fcfaf3c9'
    UPLOAD_FOLDER = 'static/uploads'
