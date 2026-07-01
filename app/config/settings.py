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

    # llm
    llm_provider: str

    llm_model: str

    llm_api_key: str

    llm_base_url: str

    llm_timeout: int

    llm_max_retry: int

    llm_temperature: float

    llm_top_p: float

    llm_max_tokens: int

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
    
    @property
    def mysql_async_url(self):

        return (
            f"mysql+aiomysql://"
            f"{self.mysql_user}:"
            f"{self.mysql_password}@"
            f"{self.mysql_host}:"
            f"{self.mysql_port}/"
            f"{self.mysql_db}"
        )

settings = Settings()