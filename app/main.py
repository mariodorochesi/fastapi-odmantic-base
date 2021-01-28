from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers.user import router as user_router
from routers.auth import router as auth_router
from utils.exceptions import MessageException

# Generate Tags descriptions
tags_metadata = [
    {
        "name": "auth",
        "description": "Operations related to account creation and managements. **Sign-Up** and **Sign-In** are included here"
    }
]

# Create FastAPI Instance
app = FastAPI(title="FastAPI Base Project",
              description="FastAPI + Odmantic base project for Mongo based applications.",
              version="0.1.0",
              openapi_tags=tags_metadata)

# Include routers
app.include_router(user_router, prefix='/users', tags=['users'])
app.include_router(auth_router, prefix='/auth', tags=['auth'])

# Add Exception Handlers
@app.exception_handler(MessageException)
async def message_exception_handler(request: Request, exc: MessageException):
    return JSONResponse(status_code=exc.status_code, content=exc.content, headers=exc.headers)
