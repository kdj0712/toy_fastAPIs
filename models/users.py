from typing import Optional, List

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

# 개발자 실수로 들어가는 field를 제한
class User(Document):
    name: Optional[str] = None
    email: Optional[EmailStr] = None # email의 규칙에 안맞으면 입력이 되지 않는다.
    pswd: Optional[str] = None
    manager: Optional[str] = None
    sellist1 : Optional[str] = None
    text : Optional[str] = None
  
    class Settings:
        name = "users"
  