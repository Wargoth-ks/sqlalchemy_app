from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    env_file: str = ".env"
    db_user: SecretStr
    db_password: SecretStr
    db_name: SecretStr


config = Settings()

os.environ["DB_USER"] = config.db_user.get_secret_value()
os.environ["DB_PASSWORD"] = config.db_password.get_secret_value()
os.environ["DB_NAME"] = config.db_name.get_secret_value()
