from fastapi import FastAPI
from routers.user import router as user_router


app = FastAPI()
app.include_router(user_router, prefix='/users')


@app.get('/')
async def root():
    return {"message": "Hello World!"}
