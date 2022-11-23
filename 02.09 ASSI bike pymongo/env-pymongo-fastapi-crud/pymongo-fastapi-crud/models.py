import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Bike(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    brand: str = Field(...)
    name: str = Field(...)
    status: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "B1",
                "brand": "Shimano",
                "name": "MTB",
                "status": "available"
            }
        }

class BikeUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    synopsis: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Shimano",
                "author": "MTB",
                "synopsis": "rented"
            }
        }