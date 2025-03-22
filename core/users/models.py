from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=150)
    password: str = Field(..., min_length=8)
    # FIXME: Use a more robust email validation! Not this nasty regex. Probably use a library.
    email: str = Field(..., pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


class UserLogin(BaseModel):
    username: str
    password: str
