from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.user import router as user_router
from routers.auth import router as auth_router
from utils.exceptions import MessageException


app = FastAPI()
app.include_router(user_router, prefix='/users', tags=['users'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])


@app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):
    return JSONResponse(status_code=exc.status_code, content=exc.content, headers=exc.headers)
