from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "there!"}


@app.get("/buildings")
def read_buildings():
    return requests.get("http://data-management/buildings").json()


@app.get("/buildings/{building}/sensors")
def read_building_sensors(building: str):
    return requests.get(f"http://data-management/buildings/{building}/sensors").json()


@app.get("/buildings/{building}/sensors/{sensor}")
def read_building_sensor(building: str, sensor: str):
    return requests.get(f"http://data-management/buildings/{building}/sensors/{sensor}").json()


@app.get("/buildings/{building}/timestamps")
def read_building_timestamps(building: str):
    return requests.get(f"http://data-management/buildings/{building}/timestamps").json()


@app.get("/algorithms")
def read_algorithms():
    return requests.get("http://anomaly-detection/algorithms").json()


@app.get("/calculate/anomalies")
def read_anomalies(algo: int, building: str, sensors: str, start: str, stop: str):
    pass


@app.get("/calculate/prototypes")
def read_prototypes(anomaly: int):
    pass


@app.get("/calculate/feature-attribution")
def read_feature_attribution(anomaly: int):
    pass
