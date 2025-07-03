from pydantic import BaseModel
from typing import Optional

# Base schema shared by both create and response
class GiftBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[float] = None

# Schema for creating a gift
class GiftCreate(GiftBase):
    pass

# Schema for returning a gift
class Gift(GiftBase):
    id: int

    class Config:
        orm_mode = True

