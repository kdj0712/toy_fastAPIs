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

# http://127.0.0.1:8000/user_api_router/
#     {
#         "name": "김덕재2",
#         "email": "kdj0712@google.com",
#         "pswd": "hijklmn",
#         "manager": "on",
#         "sellist1": "Option3",
#         "text": "만나서 반갑습니다.잘 부탁해요"
#     }

# 새로운 record 추가  = 회원가입
@router.post("/")
async def create_id(body: User) -> dict:
    document = await user_api_database.save(body)
    return {
        "message": "Event created successfully"
        ,"datas": document
    }


# http://127.0.0.1:8000/user_api_router/65974f1dc5cd3d08cca7d956/password8
# {
#     "_id": "65974f1dc5cd3d08cca7d956",
#     "name": "유재석",
#     "email": "yoojaeseok@example.com",
#     "pswd": "password8",
#     "manager": "Manager8",
#     "sellist1": "Option8",
#     "text": "안녕하세요. 유재석입니다."
# }

# id 기준으로 한 한개의 Row(record)를 가져오는 것 = 회원정보 가져오기
@router.get("/{id}/{pswd}", response_model=User)
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


# http://127.0.0.1:8000/user_api_router/65974f1dc5cd3d08cca7d956
#     {
#         "name": "김덕재",
#         "email": "kdj0712@google.com",
#         "pswd": "abcdefg",
#         "manager": "on",
#         "sellist1": "Option3",
#         "text": "만나서 반갑습니다.잘 부탁해요, 이제 집에 갑시다"
#     }


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


@router.get("/")
async def retrieve_all_ids() -> dict :
    user_apis = await user_api_database.get_all()
    return {"total_count":len(user_apis),'datas':user_apis}