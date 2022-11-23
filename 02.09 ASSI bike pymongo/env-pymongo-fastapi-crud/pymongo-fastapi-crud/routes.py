from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Bike, BikeUpdate

router = APIRouter()

@router.post("/", response_description="Create a new bike", status_code=status.HTTP_201_CREATED, response_model=Bike)
def create_bike(request: Request, bike: Bike = Body(...)):
    bike = jsonable_encoder(bike)
    new_bike = request.app.database["bikes"].insert_one(bike)
    created_bike = request.app.database["bikes"].find_one(
        {"_id": new_bike.inserted_id}
    )

    return created_bike

@router.get("/", response_description="List all bikes", response_model=List[Bike])
def list_bikes(request: Request):
    bikes = list(request.app.database["bikes"].find(limit=100))
    return bikes

@router.get("/{id}", response_description="Get a single bike by id", response_model=Bike)
def find_bike(id: str, request: Request):
    if (bike := request.app.database["bikes"].find_one({"_id": id})) is not None:
        return bike
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bikes with ID {id} not found")

@router.put("/{id}", response_description="Update a Bikes", response_model=Bike)
def update_bike(id: str, request: Request, bike: BikeUpdate = Body(...)):
    bike = {k: v for k, v in bike.dict().items() if v is not None}
    if len(bike) >= 1:
        update_result = request.app.database["bikes"].update_one(
            {"_id": id}, {"$set": bike}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bike with ID {id} not found")

    if (
        existing_bike := request.app.database["bikes"].find_one({"_id": id})
    ) is not None:
        return existing_bike

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bike with ID {id} not found")

@router.delete("/{id}", response_description="Delete a bike")
def delete_bike(id: str, request: Request, response: Response):
    delete_result = request.app.database["bikes"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Bike with ID {id} not found")

