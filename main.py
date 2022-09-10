from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    pass


@app.get("/building/{building}/sensors")
def read_building_sensors(building: str):
    pass


@app.get("/building/{building}/sensor/{sensor}")
def read_building_sensor(building: str, sensor: str):
    pass


@app.get("/building/{building}/timestamps")
def read_building_timestamps(building: str):
    pass


@app.get("/algorithms")
def read_algorithms():
    pass


@app.get("/calculate/anomalies")
def read_anomalies(algo: int, building: str, sensors: str, start: str, stop: str):
    pass


@app.get("/calculate/prototypes")
def read_prototypes(anomaly: int):
    pass


@app.get("/calculate/feature-attribution")
def read_feature_attribution(anomaly: int):
    pass
