# Backend 🎛️

The service is responsible for orchestrating all requests to the backend. It behaves like an ordinary API-gateway.

## Requirements

+ Python ≥ 3.10
+ All packages from requirements.txt

## Development

### Local

Install dependencies from requirements.txt

Start the service:

```sh
uvicorn main:app --reload
```

### Docker

We provide a docker-compose in the root directory of ADEPT to start all services bundled together.

### Available endpoints

|     | path                                     | description                                                                         |
|-----|------------------------------------------|-------------------------------------------------------------------------------------|
| GET | `/`                                      | Returns the routes available through the API                                        |
| GET | `/buildings`                             | Returns a list of buildings                                                         |
| GET | `/buildings/{building}/sensors`          | Returns a list of sensors of a specified building                                   |
| GET | `/buildings/{building}/sensors/{sensor}` | Returns the dataframe of a specified sensor                                         |
| GET | `/buildings/{building}/timestamps`       | Returns a dataframe of the data-timeframe of a specified building                   |
| GET | `/algorithms`                            | Returns a list of the available anomaly detection algorithms                        |
| GET | `/calculate/anomalies`                   | Calculates anomalies to given buildings (or dataframe) using the selected algorithm |
| GET | `/calculate/prototypes`                  | Get the prototypes for a selected anomaly                                           |
| GET | `/calculate/feature-attribution`         | Get the attribution of features for a selected anomaly                              |

Copyright © ADEPT ML, TU Dortmund 2023