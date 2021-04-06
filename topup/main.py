from database import engine
from fastapi import FastAPI
from api import models
from api.routes import user, authentication, vodafone, glo

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(vodafone.router)
app.include_router(glo.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
