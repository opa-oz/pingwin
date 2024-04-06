from fastapi import FastAPI

import influxdb_client
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS

from contextlib import asynccontextmanager

from .config import get_config, Config

global_stores = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the Influx Client and config
    cfg = get_config()
    global_stores["cfg"] = cfg
    global_stores["influx"] = influxdb_client.InfluxDBClient(url=cfg.url, username=cfg.username, password=cfg.password,
                                                             org=cfg.org)
    yield
    # Clean up the clients and release the resources
    global_stores.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root(service: str = '<unknown>', path='<unknown>'):
    client = global_stores["influx"]
    cfg: Config = global_stores["cfg"]

    if not cfg.prod:
        service = 'dev_' + service
        path = 'dev_' + path

    point = (
        Point('pinged')
        .tag('service', service)
        .tag('path', path)
        .field('name', service)
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket=cfg.bucket, org=cfg.org, record=point)

    return {'service': service, 'path': path}


@app.get("/healz")
async def healz():
    return {"message": "OK"}


@app.get("/ready")
async def ready():
    return {"message": "Ready"}
