import os

from dotenv import load_dotenv

load_dotenv()

p_name = os.getenv('DB_P_NAME')
p_host = os.getenv('DB_P_HOST')
p_port = os.getenv('DB_P_PORT')
p_user = os.getenv('DB_P_USER')
p_password = os.getenv('DB_P_PASSWORD')

test_p_name = os.getenv('TEST_DB_P_NAME')
test_p_host = os.getenv('TEST_DB_P_HOST')
test_p_port = os.getenv('TEST_DB_P_PORT')
test_p_user = os.getenv('TEST_DB_P_USER')
test_p_password = os.getenv('TEST_DB_P_PASSWORD')

secret_key = os.getenv('SECRET_KEY')
sms_email = os.getenv('SMS_EMAIL')
sms_key = os.getenv('SMS_KEY')
algorithm = os.getenv("ALGORITHM")
access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
