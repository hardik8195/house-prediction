from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils import get_location_names, load_artifacts, price_predict
from pydantic import BaseModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_artifacts()
    yield

app = FastAPI(lifespan=lifespan)


origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class independentItem(BaseModel):
    location: str
    sqft: str
    bath: str
    bhk: str


@app.get("/api/location_names")
async def location_names():
    response = {
        "location": get_location_names()
    }

    return response


@app.post("/api/predict-price")
async def prediction(item: independentItem):
    print(item)
    location = item.location
    sqft = float(item.sqft)
    bath = int(item.bath)
    bhk = int(item.bhk)
    print(location)

    result = price_predict(location, sqft, bath, bhk)
    if result is not None:
        return round(result)
    else:
        return {"message": "price prediction error"}
