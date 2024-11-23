from fastapi import FastAPI
from fastapi.params import Cookie, Header
"""
Dans cette partie nous avons vu les cookies et les headers, a noter que pour le headers, ca doit avoir des noms reconus
par les navigateur sinon on aura une valeur null
"""
app = FastAPI()

@app.get("/items")
async def read_items(
        cookie_id: str | None = Cookie(None),
        accept_encoding: str | None = Header(None),
        sec_ch_ua: str | None = Header(None),
        user_agent: str | None = Header(None)
        ):
    return {"cookie_id": cookie_id, "accept_encoding": accept_encoding, "sec_ch_ua": sec_ch_ua, "user_agent": user_agent}