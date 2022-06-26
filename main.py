from fastapi import FastAPI
from api.v1.endpoints import message, group, registration, event
from core.models import database

# metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(message.router, prefix="/message", tags=["message"])
app.include_router(group.router, prefix="/group", tags=["group"])
app.include_router(event.router, prefix="/event", tags=["event"])
app.include_router(registration.router, prefix="/registration",
                   tags=["registration"])


