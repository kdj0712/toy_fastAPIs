from typing import List
import json
from beanie import PydanticObjectId
from databases.connections import Database
from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User

router = APIRouter(
    tags=["users"]
)

user_api_database = Database(User)

# 새로운 record 추가  = 회원가입
@router.post("/")
async def create_id(body: User) -> dict:
    document = await user_api_database.save(body)
    return {
        "message": "Event created successfully"
        ,"datas": document
    }

# id 기준으로 한 한개의 Row(record)를 가져오는 것 = 회원정보 가져오기
@router.get("/{id}", response_model=User)
async def get_users_id(id: PydanticObjectId) -> User:
    users_id = await user_api_database.get(id)
    if not users_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return users_id


# ID에 따른 record의 삭제 = 회원탈퇴
@router.delete("/{id}")
async def delete_id(id: PydanticObjectId) -> dict:
    del_users = await user_api_database.get(id)
    if not del_users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    del_users = await user_api_database.delete(id)

    return {
        "message": "Event deleted successfully."
        ,"datas": del_users
    }


# 회원정보 업데이트 기능
from fastapi import Request
@router.put("/{id}", response_model=User)
async def update_id_withjson(id: PydanticObjectId, request:Request) -> User:
    user_api = await user_api_database.get(id)
    if not user_api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )
    body = await request.json()
    updated_user_api = await user_api_database.update_withjson(id, body)
    if not updated_user_api:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_user_api


# 전체 내용 가져오기
# 내가 원하는 방식으로 하려면  response_model=List[Event] 이부분을 손본다.
# @router.get("/", response_model=List[Event])
# async def retrieve_all_events() -> List[Event]:
#     events = await event_database.get_all()
#     return events


@router.get("/")
async def retrieve_all_ids() -> dict :
    user_apis = await user_api_database.get_all()
    return {"total_count":len(user_apis),'datas':user_apis}