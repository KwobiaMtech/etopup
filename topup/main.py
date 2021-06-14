from database import engine
from fastapi import FastAPI
from api import models
from api.routes import user, authentication, vodafone, glo, mtn

app = FastAPI()

app = FastAPI(
    title="E-Top Up API ",
    description="This is an EtopUp API designed to make airtime top up much easier and convenient",
    version="1.0.0",
)

models.Base.metadata.create_all(engine)

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(mtn.router)
app.include_router(vodafone.router)
app.include_router(glo.router)


@app.get("/")
def read_root():
    return {"message": "route /docs for api documentation"}
