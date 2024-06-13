from dotenv import load_dotenv
import os

class Settings:
    app_name: str = "API"
    admin_email: str = "nikit5090@gmail.com"
    DATABASE_URL: str
    POSTGRES_DATABASE_URLS: str
    POSTGRES_DATABASE_URLA: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str


settings = Settings()
settings.POSTGRES_HOST = 'db'  
settings.POSTGRES_PORT = 5432
settings.POSTGRES_PASSWORD = 'njKPyUTwLl6adBIT38aCAlpG8M695Hnq'
settings.POSTGRES_USER = 'root' 
settings.POSTGRES_DB = 'dbname_jnpp'


settings.POSTGRES_DATABASE_URLA = f"postgresql+asyncpg:" \
                                f"//{settings.POSTGRES_USER}:" \
                                f"{settings.POSTGRES_PASSWORD}" \
                                f"@{settings.POSTGRES_HOST}:" \
                                f"{settings.POSTGRES_PORT}" \
                                f"/{settings.POSTGRES_DB}"
settings.POSTGRES_DATABASE_URLS = f"postgresql:" \
                                f"//{settings.POSTGRES_USER}:" \
                                f"{settings.POSTGRES_PASSWORD}" \
                                f"@{settings.POSTGRES_HOST}:" \
                                f"{settings.POSTGRES_PORT}" \
                                f"/{settings.POSTGRES_DB}"