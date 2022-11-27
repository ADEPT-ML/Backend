from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests

anomaly_storage = dict()
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    name="Root path",
    summary="Returns the routes available through the API",
    description="Returns a route list for easier use of API through HATEOAS",
    response_description="List of urls to all available routes",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "payload": [
                            {
                                "path": "/examplePath",
                                "name": "example route"
                            }
                        ]
                    }
                }
            },
        }
    }
)
async def root():
    """Root API endpoint that lists all available API endpoints.

    Returns:
        A complete list of all possible API endpoints.
    """
    route_filter = ["openapi", "swagger_ui_html", "swagger_ui_redirect", "redoc_html"]
    url_list = [{"path": route.path, "name": route.name} for route in app.routes if route.name not in route_filter]
    return url_list


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
def read_anomalies(algo: int, building: str, sensors: str, start: str, stop: str, request: Request):
    global anomaly_storage
    uuid = request.headers.get("uuid")
    data_query = f"http://data-management/buildings/{building}/slice?{'&'.join([f'sensors={s}' for s in sensors.split(';')])}&start={start}&stop={stop}"
    building_data = requests.get(data_query).json()
    anomaly_query = f"http://anomaly-detection/calculate?algo={algo}&building={building}"
    anomalies = requests.post(anomaly_query, json=building_data).json()
    anomaly_storage[uuid] = {
        "deep-error": anomalies["deep-error"],
        "dataframe": building_data["payload"],
        "sensors": sensors.split(';'),
        "algo": algo,
        "timestamps": anomalies["timestamps"],
        "anomalies": anomalies["raw-anomalies"],
        "error": anomalies["error"]}
    del anomalies["deep-error"]
    del anomalies["raw-anomalies"]
    return anomalies


@app.get("/calculate/prototypes")
def read_prototypes(anomaly: int, request: Request):
    uuid = request.headers.get("uuid")
    return requests.post(f"http://explainability/prototypes?anomaly={anomaly}", json={"payload": anomaly_storage[uuid]}).json()


@app.get("/calculate/feature-attribution")
def read_feature_attribution(anomaly: int, request: Request):
    uuid = request.headers.get("uuid")
    return requests.post(f"http://explainability/feature-attribution?anomaly={anomaly}", json={"payload": anomaly_storage[uuid]}).json()
