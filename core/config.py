import logging
import os

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: "
           "%(filename)s: "
           "%(levelname)s: "
           "%(funcName)s(): "
           "%(lineno)d:\t"
           "%(message)s",
)
token = os.getenv('BOT_TOKEN')
channel = os.getenv('CHANNEL_ID')
channel_link = os.getenv('CHANNEL_LINK')
admin = os.getenv('ADMIN_ID')
pgip = os.getenv('POSTGRES_IP')
pguser = os.getenv('POSTGRES_USER')
pgpassword = os.getenv('POSTGRES_PASSWORD')
pgdb = os.getenv('POSTGRES_DB')
valid_domains = ['drive.yandex.ru', 'drive.google.com']

db_string = f"postgresql+psycopg2://{pguser}:{pgpassword}@{pgip}:5432/{pgdb}"
