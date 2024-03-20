from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Annotated, Union
from fastapi.responses import JSONResponse
from hashlib import sha256
from sqlalchemy.ext.asyncio import AsyncSession
from models.models_user import *
from models.dbcontext import *
from public.db import get_session
from starlette import status
from sqlalchemy import select, insert, text, update

user_router = APIRouter(tags=[Tags.users], prefix='/api/users')

# Функция для хеширования паролей
def hash_password(password: str):
    hashed_password = sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

@user_router.get("/", response_model=Union[list[Main_User], New_Respons], tags=[Tags.users])
async def get_users_db(DB: AsyncSession = Depends(get_session)):
    users = await DB.execute(select(User).order_by(User.id.asc()))
    result = users.scalars().all()
    if result == []:
        return JSONResponse(status_code=404, content={"message": "Пользователи не найдены"})
    return result

@user_router.get("/{id}", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
async def get_user(id: int, DB: AsyncSession = Depends(get_session)):
    try:
        user = await DB.execute(select(User).where(User.id == id))
        return user.scalars().one()
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    
@user_router.post("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users], status_code=status.HTTP_201_CREATED)
async def create_user(item: Annotated[Main_User, Body(embed=True, description="Новый пользователь")],
                DB: AsyncSession = Depends(get_session)):
    try:
        user = User(name=item.name, surname=item.surname, hashed_password=hash_password(item.surname), group_num=item.group_num, company_id=item.company_id)
        if user is None:
            raise HTTPException(status_code=404, detail="Объект не определён")
        await DB.execute(insert(User).values({"name": user.name, "surname": user.surname, "group_num": user.group_num, "hashed_password": user.hashed_password, "company_id": user.company_id}))
        await DB.execute(text("commit;"))
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в добавлении объекта {user}")

@user_router.put("/", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
async def edit_user(item: Annotated[Main_User, Body(embed=True, description="Изменяем данные пользователя через его id")],
                DB: AsyncSession = Depends(get_session)):
    try:   
        user = await DB.execute(select(User).where(User.id == item.id))
        result = user.scalars().one()
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        result.name = item.name
        result.surname = item.surname
        result.group_num = item.group_num
        result.company_id = item.company_id
        await DB.execute(text(f"update users set name=\'{result.name}\', surname=\'{result.surname}\', group_num=\'{result.group_num}\', company_id=\'{result.company_id}\' where id={item.id};"))
        await DB.execute(text("commit;"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в изменении объекта {result}")
    return result

@user_router.patch("/{id}", response_model=Union[Main_User, New_Respons], tags=[Tags.users])
async def edit_user_by_id(id: int, item: Annotated[Main_User, Body(embed=True, description="Изменяем данные по id")], 
                    DB: AsyncSession = Depends(get_session)):
    try:      
        user = await DB.execute(select(User).where(User.id == id))
        result = user.scalars().one()
    except Exception as e:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        new_data = item.dict(exclude_unset=True)
        if 'id' in new_data:
            del new_data['id']
        await DB.execute(update(User).values(new_data).where(User.id == id))
        await DB.execute(text("commit;"))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Произошла ошибка в изменении объекта {result}")
    return result

@user_router.delete("/{id}", response_class=JSONResponse, tags=[Tags.users])
async def delete_user(id: int, DB: AsyncSession = Depends(get_session)):
    user = await DB.execute(select(User).where(User.id == id))
    if user.first() == None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    try:
        await DB.execute(text(f'delete from users where id={id};'))
        await DB.execute(text("commit;"))
    except HTTPException:
        JSONResponse(content={"message": "Ошибка"})
    return JSONResponse(content={"message": f"Пользователь удалён {id}"})
