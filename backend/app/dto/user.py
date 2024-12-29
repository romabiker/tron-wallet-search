from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: str | None = Field(default=None, max_length=255)


class UserCreateDTO(BaseModel):
    email: EmailStr = Field(max_length=255)
    hashed_password: str
    full_name: str | None = Field(default=None, max_length=255)
    is_superuser: bool = Field(default=False)


class UserUpdateDTO(BaseModel):
    email: EmailStr = Field(max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    full_name: str | None = Field(default=None, max_length=255)
