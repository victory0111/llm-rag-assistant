from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # app
    app_name: str
    app_version: str
    debug: bool

    # llm
    model_name: str
    temperature: float = 0.7

    # mysql
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_db: str

    # redis
    redis_host: str
    redis_port: int

    embedding_model: str

    chunk_size: int

    chunk_overlap: int

    top_k: int

    class Config:
        env_file = ".env"


settings = Settings()