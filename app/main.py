from fastapi import FastAPI
from routers.user import router as user_router
from routers.auth import router as auth_router


app = FastAPI()
app.include_router(user_router, prefix='/users')
app.include_router(auth_router, prefix='/auth')


@app.get('/')
async def root():
    return {"message": "Hello World!"}
