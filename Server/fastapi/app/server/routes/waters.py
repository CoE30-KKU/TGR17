from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database.water_data import add_water_multiple 
from server.models.water import (
    ResponseModel,
    MultipleWaterSchema,
)

router = APIRouter()

@router.post("/", response_description="Add Multiple Water Data into the database")
async def add_water_data(water: MultipleWaterSchema = Body(...)):
    water = jsonable_encoder(water)
    new_water = await add_water_multiple(water["data"])
    return ResponseModel(new_water, "Water added successfully.")