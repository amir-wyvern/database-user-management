from pydantic import BaseModel, EmailStr, Field
from typing import Optional 
from enum import Enum
import re


class PhoneNumberStr(str):
    @classmethod
    def __get_pydantic_json_schema__(cls, model, context):
        return {'type': 'string', 'format': 'phonenumber', 'example': '+98-9151234567'}
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v, x):
        if not re.match(r"^\+\d{1,3}-\d{6,12}$", v):
            raise ValueError("Not a valid phone number")
        return v

class UserRole(str ,Enum):

    ADMIN = 'admin'
    USER = 'user'

class UserRegisterForDataBase(BaseModel):

    username : str
    password: str
    name : str
    email: Optional[EmailStr] = Field(default=None)
    phone_number: PhoneNumberStr
    role: UserRole