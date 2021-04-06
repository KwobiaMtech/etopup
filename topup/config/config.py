from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    APP_NAME: str = "ETOP UP API"
    POSTGRES_USER: str = os.getenv('POSTGRES_USER', 'patrick')
    POSTGRES_PASSWORD: str = os.getenv('POSTGRES_PASSWORD', 'osofo')
    POSTGRES_SERVER: str = os.getenv('POSTGRES_SERVER', '127.0.0.1:5432')
    POSTGRES_DB: str = os.getenv('POSTGRES_DB', 'topup')
    GLO_ACCOUNT_ID: str = os.getenv('GLO_ACCOUNT_ID')
    GLO_PASSWORD: str = os.getenv('GLO_PASSWORD')
    GLO_USER: str = os.getenv('GLO_USER')
    CP_ID: str = os.getenv('CP_ID')
    GLO_TOP_UP_API: str = os.getenv('GLO_TOP_UP_API')
    VODAFONE_TOP_UP_API: str = os.getenv('VODAFONE_TOP_UP_API')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
