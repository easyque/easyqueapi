from pydantic import BaseModel, Field


class OtpSend(BaseModel):
    contact: int = Field()

class User(BaseModel):
    contact: int = Field()
    is_active: bool = Field()
