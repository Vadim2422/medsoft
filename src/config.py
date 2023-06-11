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
    sms_email = os.getenv('SMS_EMAIL')
    sms_key = os.getenv('SMS_KEY')
    algorithm = os.getenv("ALGORITHM")
    access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    refresh_token_expire_minutes = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
