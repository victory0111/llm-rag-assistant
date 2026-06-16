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

    # jwt
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expire_minutes: int

    class Config:
        env_file = ".env"

    @property
    def mysql_url(self):

        return (
            f"mysql+pymysql://"
            f"{self.mysql_user}:"
            f"{self.mysql_password}@"
            f"{self.mysql_host}:"
            f"{self.mysql_port}/"
            f"{self.mysql_db}"
        )

settings = Settings()