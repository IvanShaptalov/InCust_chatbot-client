import configparser
import os
import re
from pathlib import Path
from icecream import ic

base_dir = Path(__file__).resolve().parent
config = configparser.ConfigParser()
print(base_dir)
config.read(os.path.join(base_dir, "config.ini"))


# solved create database in heroku

def database_link():
    pre_database_url = os.environ.get('DATABASE_URL') or config['DataBase']['url']
    if pre_database_url is None:
        return None
    print('database: ', pre_database_url)
    arr = re.split(pattern=r'[:|@|/]', string=pre_database_url)
    while '' in arr:
        arr.remove('')

    name = arr[4]
    print(name)
    print('info from arr ', len(arr))
    user = arr[0]
    password = arr[1]
    host_db = arr[2]
    port = arr[3]
    db_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(user, password, host_db, name)
    return db_path


BOT_TOKEN = os.environ.get('bot_token') or config['Bot']['bot_token']
PORT = os.environ.get('port') or config['Server']['port']
ALCHEMY_DB_PATH = database_link()
ic(ALCHEMY_DB_PATH)
HOST = os.environ.get('host') or config['Server']['host']
PROTOCOl = os.environ.get('protocol') or config['Server']['protocol']
MEDIA_GROUP_ID = os.environ.get('media_group_id') or config['GroupChat']['media']
SERVICE_BOT = os.environ.get('service_bot') or config['Bot']['service_bot']
# region commands
START = '/start'
MAIN_MENU = 'Главное меню'
CATALOG = 'Каталог'
ADD_EVENT = 'Добавить событие'
SKIP = 'Оставить поле пустым'
# Sure check
YES = 'да'
NO = 'нет'
# endregion
# validations
date_format = '%Y-%m-%d'
date_format_human = 'Год-месяц-день'

# callback data markers
ADD_EVENTS_PAGINATOR = 'add'
DELETE_EVENT = 'delete'
CONNECT_TO_EVENT = 'connect'

