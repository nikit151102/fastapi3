from pydantic import BaseModel, Field
from typing import Annotated, Union

class Main_User(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=0, lt=200)] = None
    name: Union[str, None] = None
    surname: Union[str, None] = None
    group_num: Union[str, None] = None
    company_id : Union[int, None] = None

class Main_UserDB(Main_User):
    hashed_password: Annotated[Union[str, None], Field(max_length=200, min_length=8)] = None

class New_Respons(BaseModel):
    message: str