"""The main module with all API definitions of the Backend service"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Path, Query, Request, HTTPException
from pydantic import Json
import requests
import json

from src import schema, validate

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


@app.get(
    "/buildings",
    name="Buildings",
    summary="Returns a list of buildings",
    description="Returns all buildings available through the building repository.\
        The response includes the buildings names.",
    response_description="List of building names.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "buildings": [
                            "EF 40",
                            "EF 40a"
                        ]
                    }
                }
            },
        }
    },
    tags=["Buildings and Sensors"]
)
def read_buildings():
    """API endpoint that returns a list of all available building names.

    Returns:
        A list of all available buildings as JSON.
    """
    try:
        response = requests.get("http://data-management/buildings")
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/buildings/{building}/sensors",
    name="Building Sensors",
    summary="Returns a list of sensors of a specified building",
    description="Returns all sensors available for the building specified through the parameter.\
        The response will include a list of the sensors with their type, desc and unit.",
    response_description="List of sensors.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "sensors": [
                            {
                                "type": "Temperatur",
                                "desc": "Wetterstation",
                                "unit": "°C"
                            },
                            {
                                "type": "Wärme Diff",
                                "desc": "Wärmeenergie Tarif 1",
                                "unit": "kWh / 15 min"
                            },
                            {
                                "type": "Wärme.5 Diff",
                                "desc": "Wärmeenergie Tarif 1",
                                "unit": "kWh / 15 min"
                            },
                            {
                                "type": "Elektrizität.1 Diff",
                                "desc": "WV+ Arbeit tariflos",
                                "unit": "kWh / 15 min"
                            },
                            {
                                "type": "Elektrizität.2 Diff",
                                "desc": "WV+ Arbeit Tarif 1",
                                "unit": "kWh / 15 min"
                            }
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Building not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Building not found"}
                }
            },
        },
    },
    tags=["Buildings and Sensors"]
)
def read_building_sensors(
        building: str = Path(
            description="Path parameter to select a building",
            example="EF 40a"
        )
):
    """API endpoint that returns a list of all available sensors.

    Args:
        building: The name of the building for which the sensors are requested.

    Returns:
        A list of all available sensors for the building or a 404 if the building is not found.
    """
    try:
        response = requests.get(f"http://data-management/buildings/{building}/sensors")
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/buildings/{building}/sensors/{sensor}",
    name="Sensor Data",
    summary="Returns the dataframe of a specified sensor",
    description="Returns the dataframe of the specified building and sensor.",
    response_description="Dataframe of the sensor.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "sensor": [
                            12.4,
                            12.1,
                            11.8,
                            11.5,
                            11.2
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Building or Sensor not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Building or Sensor not found"}
                }
            },
        }
    },
    tags=["Buildings and Sensors"]
)
def read_building_sensor(
        building: str = Path(
            description="Path parameter to select a building",
            example="EF 40a"
        ),
        sensor: str = Path(
            description="Path parameter to select a sensor",
            example="Temperatur"
        )
):
    """API endpoint that returns the data of a specific sensor of a building.

    Args:
        building: The name of the building for which the sensor values are requested.
        sensor: The name of the sensor for which the values are requested.

    Returns:
        A list of all values of the specified building sensor combination as JSON.
    """
    try:
        response = requests.get(f"http://data-management/buildings/{building}/sensors/{sensor}")
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/buildings/{building}/timestamps",
    name="Building Timeframe",
    summary="Returns a dataframe of the data-timeframe of a specified building",
    description="Returns timestamps for the specified building.",
    response_description="Dataframe of the time-data.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "timestamps": [
                            "2020-03-14T15:00:00",
                            "2020-03-14T15:15:00",
                            "2020-03-14T15:30:00",
                            "2020-03-14T15:45:00",
                            "2020-03-14T16:00:00",
                            "2020-03-14T16:15:00"
                        ]
                    }
                }
            },
        },
        404: {
            "description": "Building not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Building not found"}
                }
            },
        },
    },
    tags=["Buildings and Sensors"]
)
def read_building_timestamps(
        building: str = Path(
            description="Path parameter to select a building",
            example="EF 40a"
        )
):
    """API endpoint that returns all timestamps of the specified building.

    Args:
        building: The name of the building for which the timestamps are requested.

    Returns:
        A list of all timestamps of the available building data as JSON.
    """
    try:
        response = requests.get(f"http://data-management/buildings/{building}/timestamps")
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/algorithms",
    name="Anomaly Detection Algorithms",
    summary="Returns a list of the available anomaly detection algorithms",
    description="Returns a list with the anomaly detection algorithms..",
    response_description="List of the algorithms.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "algorithms": [
                            {
                                "name": "Isolation Forest",
                                "id": 0,
                                "explainable": False,
                                "config": {
                                    "settings": []
                                }
                            },
                            {
                                "name": "One-Class SVM",
                                "id": 1,
                                "explainable": False,
                                "config": {
                                    "settings": []
                                }
                            },
                            {
                                "name": "LSTM Autoencoder",
                                "id": 2,
                                "explainable": False,
                                "config": {
                                    "settings": []
                                }
                            }
                        ]
                    }
                }
            },
        },
    },
    tags=["Anomaly Detection"]
)
def read_algorithms():
    """API endpoint that returns a list of all available anomaly detection algorithms.

    Returns:
        A list of all anomaly detection algorithms including their configuration options.
    """
    try:
        response = requests.get("http://anomaly-detection/algorithms")
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/calculate/anomalies",
    name="Calculate anomalies",
    summary="Calculates anomalies to given buildings (or dataframe) using the selected algorithm",
    description="Returns a list of anomalies and accompanying information.",
    response_description="List of anomalies.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "error": [0.03145960019416866, 0.024359986113175414, 0.023060245303469007],
                        "timestamps": ["2020-03-14T11:00:00", "2020-03-14T11:15:00", "2020-03-14T11:30:00"],
                        "anomalies": [
                            {"timestamp": "2021-12-21T09:45:00", "type": "Area"},
                            {"timestamp": "2021-12-22T09:45:00", "type": "Area"}
                        ],
                        "threshold": 0.2903343708384869
                    }
                }
            },
        },
        404: {
            "description": "Algorithm or Building not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Building not found"}
                }
            },
        },
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            },
        }
    },
    tags=["Anomaly Detection"]
)
def read_anomalies(
        algo: int = Query(
            description="Path parameter to select the algorithm",
            example="1"
        ),
        building: str = Query(
            description="Query parameter to select a building",
            example="EF 40a"
        ),
        sensors: str = Query(
            description="Query parameter list to select the sensors. \
        The list has to be seperated by ; and all sensors have to be available sensors for the selected building.",
            example="Temperatur;Wärme Diff"
        ),
        start: str = Query(
            description="Query parameter to select the start of the timeframe. \
        The timestamp has to be inside of the dataframe of the building + sensors combination",
            example="2021-01-01T23:00:00.000Z"
        ),
        stop: str = Query(
            description="Query parameter to select the end of the timeframe. \
        The timestamp has to be inside of the dataframe of the building + sensors combination",
            example="2022-01-01T23:00:00.000Z"
        ),
        config: Json = Query(
            description="Query parameter to send a config for the algo",
            example={"dropdown": "Percentile", "percentile": 99.5, "constant": 1}
        ),
        request: Request = None
):
    """API endpoint that analyzes the specified data slice and detects anomalies within.

    Args:
        algo: The id of the desired algorithm.
        building: The name of the building.
        sensors: The desired selection of sensors.
        start: The first timestamp of the data slice.
        stop: The last timestamp of the data slice.
        config: The configuration for the algorithm.
        request: The request object containing the uuid.

    Returns:
        A json representation of the identified anomalies and additional metadata.
    """
    try:
        global anomaly_storage
        uuid = request.headers.get("uuid")
        sensors_list = sensors.split(';')
        sensors_parameter = '&'.join([f'sensors={s}' for s in sensors_list])
        data_url = f"http://data-management/buildings/{building}/slice?{sensors_parameter}&start={start}&stop={stop}"
        building_data = requests.get(data_url)
        validate.validate_response(building_data)
        building_data = building_data.json()
        anomaly_url = f"http://anomaly-detection/calculate?algo={algo}&building={building}&config={json.dumps(config)}"
        anomalies_response = requests.post(anomaly_url, json=building_data)
        validate.validate_response(anomalies_response)
        anomalies = anomalies_response.json()
        anomaly_storage[uuid] = {
            "deep-error": anomalies["deep-error"],
            "dataframe": building_data["payload"],
            "sensors": sensors_list,
            "algo": algo,
            "timestamps": anomalies["timestamps"],
            "anomalies": anomalies["raw-anomalies"],
            "error": anomalies["error"]
        }
        del anomalies["deep-error"]
        del anomalies["raw-anomalies"]
        return anomalies
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/calculate/prototypes",
    name="Get prototypes for a selected anomaly",
    summary="Get the prototypes for a selected anomaly",
    description="Returns a dict with two prototypes and the original anomaly.",
    response_description="Dict of prototypes and anomalies.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "prototypes": {
                            "prototype a": [
                                0.01675, 0.01675, 0.01675, 0.01675, 0.07375, 0.07375, 0.07375, 0.07375, 0.0315, 0.0315,
                                0.0315, 0.0315, 0.049, 0.049, 0.049, 0.049, 0.034, 0.034, 0.034, 0.034, 0.052, 0.052,
                                0.052, 0.052, 0.063, 0.063, 0.063, 0.063, 0.07175, 0.07175, 0.07175, 0.07175, 0.06775
                            ],
                            "prototype b": [
                                0.004, 0.004, 0.004, 0.004, 0.00275, 0.00275, 0.00275, 0.00275, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.0, 0.0
                            ],
                            "anomaly": [
                                0.0055, 0.0055, 0.0055, 0.0055, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                                0.0, 0.4355, 0.4355, 0.4355, 0.4355, 0.09325, 0.09325, 0.09325, 0.09325, 0.00025,
                                0.00025, 0.00025, 0.00025, 0.0, 0.0, 0.0, 0.0, 0.0
                            ]
                        }
                    }
                }
            },
        },
        400: {
            "description": "Payload can not be empty.",
            "content": {
                "application/json": {
                    "example": {"detail": "Payload can not be empty"}
                }
            },
        },
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            },
        }
    },
    tags=["Prototypes"]
)
def read_prototypes(
        anomaly: int = Query(
            description="Path parameter to select the algorithm",
            example="1"
        ),
        request: Request = None
):
    """API endpoint that creates prototypes for the specified anomaly.

    Args:
        anomaly: The ID of the anomaly for which the prototypes are created.
        request: The request object containing the uuid.

    Returns:
        Two created prototypes and the anomaly with the same timeframe.
    """
    try:
        uuid = request.headers.get("uuid")
        url = f"http://explainability/prototypes?anomaly={anomaly}"
        response = requests.post(url, json={"payload": anomaly_storage[uuid]})
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get(
    "/calculate/feature-attribution",
    name="Get attribution of features for a selected anomaly",
    summary="Get the attribution of features for a selected anomaly",
    description="Returns a a list with the names and percentages of the feature attribution.",
    response_description="A list with the names and percentages of feature attribution.",
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": {
                        "attribution": [
                            {'name': 'Wasser.1 Diff', 'percent': 82.65603968422548},
                            {'name': 'Elektrizität.1 Diff', 'percent': 17.343960315774527}
                        ]
                    }
                }
            },
        },
        400: {
            "description": "Payload can not be empty.",
            "content": {
                "application/json": {
                    "example": {"detail": "Payload can not be empty"}
                }
            },
        },
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            },
        }
    },
    tags=["Attributions"]
)
def read_feature_attribution(
        anomaly: int = Query(
            description="Path parameter to select the algorithm",
            example="1"
        ),
        request: Request = None
):
    """API endpoint that calculates the feature attribution for the specified anomaly.

    Args:
        anomaly: The ID of the anomaly for which the prototypes are created.
        request: The request object containing the uuid.

    Returns:
        The calculated feature attribution for the specified anomaly.
    """
    try:
        uuid = request.headers.get("uuid")
        url = f"http://explainability/feature-attribution?anomaly={anomaly}"
        response = requests.post(url, json={"payload": anomaly_storage[uuid]})
        validate.validate_response(response)
        return response.json()
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")


schema.custom_openapi(app)
