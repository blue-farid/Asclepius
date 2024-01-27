from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str
    health_check_time: int
    app_port: int

    class Config:
        env_file = ".env"


settings = Settings()
