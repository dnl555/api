from fastapi import APIRouter, status, Body
from fastapi.responses import JSONResponse, Response
from datetime import date
from api.decorators import validate_username_and_dateofbirth
from app.core.db import User, Session


router = APIRouter()


@router.put(
    "/hello/{username}",
    summary="PUT Simple Hello World",
)
@validate_username_and_dateofbirth
async def put_hello(
    username: str,
    payload: dict = Body(default={}),
):

    try:
        user_payload = User(username=username, date_of_birth=payload["dateOfBirth"])
        user = Session.query(User).filter(User.username == username).first()
        if user:
            user.date_of_birth = user_payload.date_of_birth
        else:
            Session.add(user_payload)
        Session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except:
        Session.rollback()
        raise
    finally:
        Session.close()


@router.get(
    "/hello/{username}",
    summary="GET Simple Hello World",
)
async def get_hello(
    username: str,
):

    user = Session.query(User).filter(User.username == username).first()
    if user:

        # calculate days to birthday
        current_year_birthday = date(
            date.today().year, user.date_of_birth.month, user.date_of_birth.day
        )

        # birthday already passed, let's calculate for next year
        if current_year_birthday < date.today():
            current_year_birthday = current_year_birthday.replace(
                year=date.today().year + 1
            )

        days_to_birthday = (current_year_birthday - date.today()).days

        if days_to_birthday == 0:
            return JSONResponse(
                content={"message": f"Hello, {username}! Happy birthday!"},
                status_code=status.HTTP_200_OK,
            )
        else:
            return JSONResponse(
                content={
                    "message": f"Hello, {username}! Your birthday is in {days_to_birthday} day(s)"
                },
                status_code=status.HTTP_200_OK,
            )
    else:
        return JSONResponse(
            content={"error_msg": "user not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
