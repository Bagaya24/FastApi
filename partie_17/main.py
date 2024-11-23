from fastapi import FastAPI, File, UploadFile
from starlette.responses import HTMLResponse

"""
Dans cette partie, nous avons vu comment les classes qui nous permettent de manipuler les fichier, ces classes sont
'File' et 'UploadFile' mais de preference vaut mieux utiliser 'UploadFile' vue que ca nous donne beaucoup plus d'information
sur les fichiers
"""
app = FastAPI()

@app.post("/files")
async def create_file(file: bytes | None = File(None)):
    if not file:
        return {"message": "not file sent"}
    return {"file": len(file)}

@app.post("/uploadfile")
async def create_upload_file(files: list[UploadFile]):
    return {"file": [file.filename for file in files]}

@app.get("/")
async def main():
    return HTMLResponse(content="<h1>hello</h1>")
