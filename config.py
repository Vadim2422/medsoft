import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    p_name = os.getenv('DB_P_NAME')
    p_host = os.getenv('DB_P_HOST')
    p_port = os.getenv('DB_P_PORT')
    p_user = os.getenv('DB_P_USER')
    p_password = os.getenv('DB_P_PASSWORD')
    secret_key = os.getenv('SECRET_KEY')
    algorithm = os.getenv("ALGORITHM")
    access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
