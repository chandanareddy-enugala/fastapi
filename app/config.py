from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str 
    database_username: str =  "postgres"
    secret_key: str
    
    access_token_expire_minutes: int
    algorithm: str
    
    class Config:
        env_file ="app/.env"
    

settings = Settings()
print("password" , settings.database_password)
