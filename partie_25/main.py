from fastapi import FastAPI, HTTPException, Depends
from fastapi.params import Header

"""
Dans cette partie, nous vouillons que c'est possible de mettre les dependances dans un decorateur, la grande difference
entre les mettre sur un decorateur et sur une fonction est que dans un decorateur, ca ne sert qu'a verifier certaine 
chose, on a pas besoin de la valeur qu'elle retourne depend que dans une fonction, on a besoin de la valeur qu'elle 
retourne. L'attribue 'dependencies' permet de mettre les dependances dans le decorateur, si on veut que certaines 
dependances soient dans tout nos routes, il suffirait de le dans 'app=FastAPI(dependencies=[dependances]'
"""
app = FastAPI()

async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-token header invalid")

async def verify_key(x_key: str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="x_key header invalid")

@app.get("/items", dependencies=[Depends(verify_key), Depends(verify_token)])
async def read_items():
    return {"Item": "Foo"}