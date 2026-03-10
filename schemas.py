from pydantic import BaseModel
from typing import Optional

# Lo que enviamos (Request)
class ContractorCreate(BaseModel):
    company_name: str
    contact_name: Optional[str] = None
    services: Optional[str] = None

# Lo que la API responde (Response)
class Contractor(ContractorCreate):
    id: int
    average_rating: float = 0.0 # <--- Lo que muestra el promedio

    class Config:
        from_attributes = True

class ReviewCreate(BaseModel):
    contractor_id: int
    availability: int
    coordination: int
    cost_effectiveness: int
    skill_level: int
    reliability: int
    comments: Optional[str] = None

class Review(ReviewCreate):
    id: int
    
    class Config:
        from_attributes = True

class ContractorUpdate(BaseModel):
    company_name: Optional[str] = None
    contact_name: Optional[str] = None
    services: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str # Password that the user enters

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True