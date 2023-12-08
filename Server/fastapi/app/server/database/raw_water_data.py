import motor.motor_asyncio
from bson.objectid import ObjectId
from server.my_config import MONGODB_CONN
import time

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_CONN)

database = client["TGR2023"]

water_collection = database.get_collection("raw_water_data")

def water_helper(water) -> dict:
    return {
        "id": str(water["_id"]),
        "name": water["name"],
        "height": water["height"],
        "time": water["time"]
        # "discharge_rate": water["discharge_rate"],
        # "waterfront": water["waterfront"],
        # "waterback": water["waterback"],
        # "waterdrain": water["waterdrain"],
    }

# Retrieve all waters present in the database
async def retrieve_waters():
    waters = []
    async for water in water_collection.find():
        waters.append(water_helper(water))
    return waters

# Retrieve all waters present in the database
async def retrieve_waters_by_name(name):
    waters = []
    async for water in water_collection.find({"name": name}):
        waters.append(water_helper(water))
    return waters

# Add a new water into to the database
async def add_water(water_data: dict) -> dict:
    water_data["time"] = time.time()
    water = await water_collection.insert_one(water_data)
    new_water = await water_collection.find_one({"_id": water.inserted_id})
    return water_helper(new_water)

async def add_water_multiple(water_data_list: list) -> list:
    for i in range(0, len(water_data_list)):
        water_data_list[i]["time"] = time.time()
    water = await water_collection.insert_many(water_data_list)
    new_water = await water_collection.find({"_id": {"$in": water.inserted_ids}})
    water_list = []
    async for w in new_water:
        water_list.append(water_helper(w))
    return water_list

# Retrieve a water data with a matching ID
async def retrieve_water(id: str) -> dict:
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        return water_helper(water)


# Update a water with a matching ID
async def update_water(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        updated_water = await water_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_water:
            return True
        return False


# Delete a water from the database
async def delete_water(id: str):
    water = await water_collection.find_one({"_id": ObjectId(id)})
    if water:
        await water_collection.delete_one({"_id": ObjectId(id)})
        return True