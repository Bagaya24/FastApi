from fastapi import FastAPI

"""
Dans cette partie, nous avons vu comment ajouter des metadatas dans notre API, ca peut rendre notre API beaucoup plus 
professionnelle.
"""

description = """
    ChimichanApp API help you to do awesome stuff.
    ## items
    You can **read items**
    
    ## Users
    You will be able to:
    * **create users** (_not implemented_).
    * **read users** (_not implemented_).
    
    """

tags_metadata = [
    {"name": "users", "description": "Operations with users. The **login** logic is also here."},
    {"name": "items", "description": "Manage items. So _fancy_ they have their own docs",
     "externalDocs": {
         "description": "Items external docs", "url": "https://ww.jsv/design"
     }
     },

]
app = FastAPI(
    title="ChimiChanApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://exemple.com/terms",
    contact=dict(
        name="MrBoy",
        url="http://mrboy.exemple.cd/contact",
        email = "bagayafazili@gmail.com"
    ),
    license_info=dict(
        name="Apache 2.0",
        url="https://www.apache.org/licenses"
    ),
    openapi_tags=tags_metadata,
    openapi_url="/api/v1/openapi.json",
    docs_url="/hello"

)

@app.get("/users", tags=["users"])
async def get_users():
    return [{"name": "Cole"}, {"name": "Palmer"}]

@app.get("/items", tags=["items"])
async def read_items():
    return [{"name": "wand"}, {"name": "flying broom"}]