import os


class ENV:
    @staticmethod
    def get(key: str, default=None):
        return os.getenv(key, default)

    @staticmethod
    def set(key: str, value: str):
        os.environ[key] = value

    @staticmethod
    def db_provider() -> str:
        return ENV.get("DB_PROVIDER", "sqlite")

    @staticmethod
    def db_url() -> str:
        return ENV.get("DB_PATH", "./db/db.sqlite3")
