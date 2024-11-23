from fastapi import FastAPI, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError, StarletteHTTPException
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from starlette.responses import JSONResponse, PlainTextResponse

"""
Dans cette partie, nous avons vue que c'est possible de traquer nous meme les erreurs mais que c'est aussi possible de
creer de fonction qui vont nous dire de quel erreur il s'agit, erreurs qui sont souvent causer par l'utisateur,
il y'a 'RequestValidationError' qui permet de signifier a l'utilisateur qu'il se tromper de type ou qu'il y'a un probleme
au niveau de donner du client et 'StarletteHTTPException' qui permet de signifier a l'utilisateur qu'il a un probleme 
avec le HTTP
"""
app = FastAPI()

items = {"foo": "The foo wrestlers"}
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in items:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found", headers={"x-Error": "There goes my error"})
#     return {"item": items[item_id]}

class UniCornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UniCornException)
async def unicorn_exception_handler(request: Request, exc: UniCornException):
    return JSONResponse(status_code=status.HTTP_418_IM_A_TEAPOT, content={"message": f"Opps {exc.name} did something"})

@app.get("/unicorn/{name}")
async def read_unicorn(name: str):
    if name == "yole":
        raise UniCornException(name=name)
    return {"unicorn": name}
#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)
#
# @app.exception_handler(StarletteHTTPException)
# async def http_exception(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
#
# @app.get("/validation_item/{item_id}")
# async def read_validation_items(item_id: int):
#     if item_id == 1:
#         raise HTTPException(status_code=status.HTTP_410_GONE, detail="Nope")
#     return {"item_id": item_id}

#
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#                         content=jsonable_encoder({"detail": exc.errors(),
#                                                   "body": exc.body})
#                         )
# class Item(BaseModel):
#     title: str
#     size: float
#
# @app.post("/items")
# async def create_item(item: Item):
#     return item

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"HTTP error: {repr(exc)}")
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"the client send invalid data!{exc}")
    return await request_validation_exception_handler(request, exc)

@app.get("/items/{item_id}")
async def read_items(item_id: int):
    if item_id == 2:
        raise HTTPException(status_code=410, detail="NOPE!")
    return {"item_id": item_id}