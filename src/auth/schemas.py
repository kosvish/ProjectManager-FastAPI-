from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    class ConfigDict:
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

    class ConfigDict:
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

    class ConfigDict:
        from_attributes = True


class UserResponse(BaseModel):
    username: str
    email: str
    hashed_password: str



