from fastapi import HTTPException


def handle_response(response):

    if 200 <= response.status_code < 300:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
