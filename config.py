class Config:
    SECRET_KEY = "dev-secret-key-123" # Required for flash messages and sessions
    SQLALCHEMY_DATABASE_URI = "sqlite:///cms.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False