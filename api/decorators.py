import functools
import inspect

from fastapi.responses import JSONResponse
from fastapi import status
from datetime import datetime, timedelta


def validate_username_and_dateofbirth(func):
    @functools.wraps(func)
    async def wrap_func(*args, **kwargs):

        # username must contain only letters
        if not kwargs["username"].isalpha():
            return JSONResponse(
                content={"error_msg": "username must contain only letters"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # dateofbirth must exist
        if "dateOfBirth" not in kwargs["payload"]:
            return JSONResponse(
                content={"error_msg": "you must specify dateOfBirth"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # dateofbirth must be string
        if not isinstance(kwargs["payload"]["dateOfBirth"], str):
            return JSONResponse(
                content={"error_msg": "dateOfBirth must be string"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # dateofbirth must be in the format YYYY-MM-DD
        try:
            datetime.strptime(kwargs["payload"]["dateOfBirth"], "%Y-%m-%d")
        except ValueError:
            return JSONResponse(
                content={
                    "error_msg": "dateOfBirth is not valid, use the format YYYY-MM-DD"
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # dateofbirth must be a date before the today date
        if datetime.strptime(
            kwargs["payload"]["dateOfBirth"], "%Y-%m-%d"
        ) > datetime.now() - timedelta(days=1):
            return JSONResponse(
                content={
                    "error_msg": "dateOfBirth must be a date before the today date"
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Handle async and non-async functions
        if inspect.iscoroutinefunction(func):
            result = await func(*args, **kwargs)
        else:
            result = func(*args, **kwargs)

        return result

    return wrap_func
