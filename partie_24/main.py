from fastapi import FastAPI, Depends, Body
"""
Dans cette partie, nous avons vue un exemple ou la fonction 'try_query' depend de la valeur de retour
de 'query_or_body_exctactor' qui elle aussi depend de la valeur de retour de la fonction 'query_extractor'.
D'une certaine maniere 'try_query' appelle la fonction 'query_or_body_extractor' qui appelle aussi la fonction
'query_extractor'.
"""
app = FastAPI()

def query_extractor(q: str | None = None):
    return q

def query_or_body_extractor(q: str = Depends(query_extractor), last_query: str | None = Body(None)):
    if not q:
        return last_query
    return q

@app.post("/items/")
async def try_query(query_body: str = Depends(query_or_body_extractor)):
    return {"query_or_body": query_body}