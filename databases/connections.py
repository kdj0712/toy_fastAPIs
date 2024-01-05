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

class Database:
    # model = collection
    def __init__(self,model) -> None:
        self.model = model
        pass
    
    # 전체 리스트
    async def get_all(self):
        documents = await self.model.find_all().to_list() # find({})과 거의 같은 기능
        pass
        return documents
    
    # 상세 보기
    async def get(self, id: PydanticObjectId) -> Any:
        doc = await self.model.get(id) # find_one()과 거의 같은 기능
        if doc:
            return doc
        return False
    
    # 저장
    async def save(self, document) -> None:
        await document.create()
        return None