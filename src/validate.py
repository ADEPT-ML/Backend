from fastapi import HTTPException
from requests import Response


def validate_response(response: Response) -> Response:
    """Validates the response object of http requests.

    Args:
        response: The output of http requests

    Returns:
        The response or an HTTPException
    """
    status_code = response.status_code
    if status_code == 200:
        return response
    response_json = response.json()
    message = response_json["detail"] if "detail" in response_json else f"{status_code}"
    raise HTTPException(status_code=status_code, detail=message)
