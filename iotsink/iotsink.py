import sys
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict

from .core.Logger import Logger
from .Handler import Handler



app = FastAPI()


def on_starting(iotsink):
    Logger.log(__name__, 'loading server app worker')
    if not Handler.load():
        Logger.log(__name__, 'cloud not load server app worker, exiting', type='error')
        sys.exit(1)
    Logger.log(__name__, 'server app worker loaded successfully')


class RoutePost(BaseModel):

    type: str
    source: str
    data: Dict

    class Config:
        schema_extra = {
            "example": 	{
		        "type": "event", 
                "source": "A_SOURCE", 
                "data": {"movement": "true"}
	        }
        }


class LoadTestPost(BaseModel):

    type: str
    source: str
    data: Dict

    class Config:
        schema_extra = {
            "example": 	{
		        "type": "load_test",
                "source": "load_tester", 
                "data": {"cpu": 100, "io": 0.04}
	        }
        }


@app.get("/")
async def get_root(request: Request):
    Logger.log(__name__, '{host}:{port} - "{method} {path} {scheme}"'.format(host=request.client.host, 
                                                                          port=request.client.port, 
                                                                          method=request.method, 
                                                                          path=request.url.path,
                                                                          scheme=request.url.scheme))
    return {"msg": "iotsink service"}



@app.get("/check")
async def get_check(request: Request):
    Logger.log(__name__, '{host}:{port} - "{method} {path} {scheme}"'.format(host=request.client.host, 
                                                                          port=request.client.port, 
                                                                          method=request.method, 
                                                                          path=request.url.path,
                                                                          scheme=request.url.scheme))
    return 'OK'.encode('utf-8')


@app.post("/route")
async def post_route(route_post : RoutePost):

    request = dict(route_post)

    request['timestamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

    Logger.log(__name__, 'post route request: {request}'.format(request=request))

    Handler.handle(request)

    return {"status": "OK"}


@app.post("/load_test")
async def post_load_test(load_test_post : LoadTestPost):

    request = dict(load_test_post)

    request['timestamp'] = datetime.utcnow().replace(tzinfo=timezone.utc).timestamp()

    Logger.log(__name__, 'post load test request: {request}'.format(request=request))

    Handler.handle(request)

    return {"status": "OK"}

