from typing import Tuple

from app.fastapi_users import auth_backend, fastapi_users, get_user_manager
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import models
from fastapi_users.authentication import Strategy
from fastapi_users.manager import BaseUserManager
from fastapi_users.openapi import OpenAPIResponseType
from fastapi_users.router.common import ErrorCode, ErrorModel

backend = auth_backend
authenticator = fastapi_users.authenticator
requires_verification: bool = False

router = APIRouter()

get_current_user_token = authenticator.current_user_token(
    active=True, verified=requires_verification
)


login_responses: OpenAPIResponseType = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorModel,
        "content": {
            "application/json": {
                "examples": {
                    ErrorCode.LOGIN_BAD_CREDENTIALS: {
                        "summary": "Bad credentials or the user is inactive.",
                        "value": {"detail": ErrorCode.LOGIN_BAD_CREDENTIALS},
                    },
                    ErrorCode.LOGIN_USER_NOT_VERIFIED: {
                        "summary": "The user is not verified.",
                        "value": {"detail": ErrorCode.LOGIN_USER_NOT_VERIFIED},
                    },
                }
            }
        },
    },
    **backend.transport.get_openapi_login_responses_success(),
}


@router.post(
    "/jwt/login",
    name=f"auth:{backend.name}.login",
    responses=login_responses,
)
async def login(
    request: Request,
    response: Response,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
        )
    if requires_verification and not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.LOGIN_USER_NOT_VERIFIED,
        )
    login_return = await backend.login(strategy, user, response)
    await user_manager.on_after_login(user, request)
    resp_body = login_return.dict()
    resp_body["role"] = user.role
    return resp_body


logout_responses: OpenAPIResponseType = {
    **{
        status.HTTP_401_UNAUTHORIZED: {"description": "Missing token or inactive user."}
    },
    **backend.transport.get_openapi_logout_responses_success(),
}


@router.post(
    "/jwt/logout", name=f"auth:{backend.name}.logout", responses=logout_responses
)
async def logout(
    response: Response,
    user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
    strategy: Strategy[models.UP, models.ID] = Depends(backend.get_strategy),
):
    user, token = user_token
    return await backend.logout(strategy, user, token, response)
