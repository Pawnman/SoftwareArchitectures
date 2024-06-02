from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "messenger_db"
    MONGO_HOST: str = "mongo"
    MONGO_INITDB_ROOT_USERNAME: str = "mongo"
    MONGO_INITDB_ROOT_PASSWORD: str = "mongo123"
    API_GATEWAY_URL: str = "http://api_gateway:8000"
    USER_SERVICE_URL: str = "http://user_microservice:8100"
    PTP_CHAT_SERVICE_URL: str = "http://ptp_chat_microservice:8090"
    GROUP_CHAT_SERVICE_URL: str = "http://group_chat_microservice:8070"
    SECRET_KEY_AUTH: str = "efewf3@1fwefw!edwgweerg"
    SECRET_KEY_JWT: str = "21423rEFEWF2e1vDG21"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


settings = Settings()
