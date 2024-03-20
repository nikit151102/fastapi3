from pydantic import BaseModel, Field
from typing import Annotated, Union

class Main_Company(BaseModel):
    id: Annotated[Union[int, None], Field(default=100, ge=0, lt=200)] = None
    name: Union[str, None] = None
    country: Union[str, None] = None

class New_Respons(BaseModel):
    message: str