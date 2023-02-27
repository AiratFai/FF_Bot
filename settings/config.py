from dataclasses import dataclass
import os
import dotenv

dotenv.load_dotenv()  # Для загрузки токена в окружение.


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    users_ids: list[int]  # Список id администраторов бота


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig


config = Config(tg_bot=TgBot(token=os.getenv('bot_token'),
                             users_ids=list(map(int, os.getenv('users').split(', ')))),
                db=DatabaseConfig(database=os.getenv('DATABASE'),
                                  db_host=os.getenv('DB_HOST'),
                                  db_user=os.getenv('DB_USER'),
                                  db_password=os.getenv('DB_PASSWORD')))
