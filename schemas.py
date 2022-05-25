from pydantic import BaseModel, Field


class OtpSend(BaseModel):
    contact: int = Field()

class User(BaseModel):
    contact: int = Field()
    is_active: bool = Field()
    auth_token: str = Field(min_length=2)
