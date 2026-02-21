from pydantic import BaseModel

class FAQBase(BaseModel):
    question: str
    answer: str

class FAQCreate(FAQBase):
    pass

class FAQ(FAQBase):
    id: int

    class Config:
        from_attributes = True

class FAQAskRequest(BaseModel):
    question: str

class FAQAskResponse(BaseModel):
    answer: str
