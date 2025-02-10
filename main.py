from fastapi import FastAPI
from app.api.routes import router
import uvicorn

from fastapi.staticfiles import StaticFiles #test

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    app.mount("/static", StaticFiles(directory="static"), name="static") #tesd
    uvicorn.run(app, host="0.0.0.0", port=8000)
