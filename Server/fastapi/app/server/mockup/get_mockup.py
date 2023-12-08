import datetime
import requests
import json
from fastapi import APIRouter
from server.models.water import (ResponseModel, ErrorResponseModel)
from server.database.water_data import (add_water,add_water_multiple)

router = APIRouter()

@router.get("/", response_description="Water Data Retrieved")
async def get_mockup():
    url = f'http://192.168.1.3:7078/'
    mockup = requests.get(url)
    if mockup:
        print(json.loads(mockup.text))
        return ResponseModel(json.loads(mockup.text), f"API data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Data doesn't exist.")

@router.get("/{id}", response_description="Water Data Retrieved")
async def get_mockup_data(id):
    url = f'http://192.168.1.3:7078/{id}'
    mockup = requests.get(url)
    if mockup:
        print(json.loads(mockup.text))
        return ResponseModel(json.loads(mockup.text), f"API data ID: {id} retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Data doesn't exist.")

@router.get("/range/{startId}-{endId}", response_description="Multi Water Data Retrieved")
async def get_mockup_data(startId: int, endId: int):
    if startId > endId:
        return ErrorResponseModel("An error occurred.", 400, "Bad Request: Start ID is greather than End ID")
    data = []
    error = None
    for id in range(startId, endId):
        url = f'http://192.168.1.3:7078/{id}'
        mockup = requests.get(url)
        if mockup:
            data.append(json.loads(mockup.text)[0])
        else:
            error = ErrorResponseModel("An error occurred.", 404, "Data doesn't exist.")
    if error:
        return error
    return ResponseModel(data, f"API data ID: {startId} - {endId} retrieved successfully")

# TODO: test
@router.get("/getSave/{id}", response_description="Multi Water Data Retrieved and Save to DB")
async def get_mockup_data(id: int):
    url = f'http://192.168.1.3:7078/{id}'
    mockup = requests.get(url)
    if mockup:
        rr = json.loads(mockup.text)[0]
        date_str = rr["w_date"]
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        year = date_obj.year
        month = date_obj.month
        day = date_obj.day
        w_height = rr["w_height"]
        w_cubic = rr["w_cubic"]
        js = {
            'name': f"id_{id}",
            'year': year,
            'month': month,
            'date': day,
            'waterfront': w_height,
            'waterback': w_cubic,
            'waterdrain': round(abs(w_height-w_cubic),1)
        }
        await add_water(js)
        return ResponseModel(rr, f"API data ID: {id} retrieved and added successfully")
    else:
        return ErrorResponseModel("An error occurred.", 404, "Data doesn't exist.")

# TODO: test
@router.get("/getSave/{startId}-{endId}", response_description="Multi Water Data Retrieved and Save to DB")
async def get_mockup_data(startId: int, endId: int):
    if startId > endId:
        return ErrorResponseModel("An error occurred.", 400, "Bad Request: Start ID is greather than End ID")
    data = []
    error = None
    for id in range(startId, endId):
        url = f'http://192.168.1.3:7078/{id}'
        mockup = requests.get(url)
        if mockup:
            rr = json.loads(mockup.text)[0]
            date_str = rr["w_date"]
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            year = date_obj.year
            month = date_obj.month
            day = date_obj.day
            w_height = rr["w_height"]
            w_cubic = rr["w_cubic"]
            js = {
                'name': f"id_{id}",
                'year': year,
                'month': month,
                'date': day,
                'waterfront': w_height,
                'waterback': w_cubic,
                'waterdrain': round(abs(w_height-w_cubic),1)
            }
            data.append(js)
        else:
            error = ErrorResponseModel("An error occurred.", 404, "Data doesn't exist.")
    if error:
        return error
    await add_water_multiple(data)
    return ResponseModel(data, f"API data ID: {startId} - {endId} retrieved successfully")

