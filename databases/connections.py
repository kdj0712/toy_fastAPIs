from typing import Any, List, Optional
from beanie import init_beanie, PydanticObjectId
from models.users import User
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None


    async def initialize_database(self): # 비동기화 되어 있으므로 즉각적인 반응이 있지는 않지만, 업무 자체는 완료할 수 있도록 한다.
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(database=client.get_default_database(),
                          document_models=[User])
        
    class Config:
        env_file = ".env"