from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "John Doe",
                "email": "johndoe@example.com",
                "password": "password"
            }
        }


class LoginUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "johndoe@example.com",
                "password": "password"
            }
        }


class User(BaseModel):
    id: int
    username: str
    email: str
    password: str
    authenticated: bool = False
    role_id: int
    role: str

    class Config:
        from_attributes = True






