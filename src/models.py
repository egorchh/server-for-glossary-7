from pydantic import BaseModel, Field
from typing import Optional

class TermBase(BaseModel):
    term: str = Field(..., min_length=1, description="Термин для глоссария")
    description: str = Field(..., min_length=1, description="Описание термина")

class TermCreate(TermBase):
    pass

class TermUpdate(BaseModel):
    term: Optional[str] = Field(None, min_length=1, description="Обновленный термин")
    description: Optional[str] = Field(None, min_length=1, description="Обновленное описание")

class Term(TermBase):
    id: int
    
    class Config:
        from_attributes = True 