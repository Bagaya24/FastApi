from fastapi import FastAPI, UploadFile, File, Form
"""
Dans cette partie, nous vouillons que nous pouvons faire un form qui a a la fois la possibilite de gerer les fichier
mais aussi les texts. A noter que si  nous melangeons le doby query et le Form, le navigateur va transformer les body 
query en Form.
"""
app = FastAPI()

@app.post("/files/")
async def create_file(file: bytes= File(...), fileb: UploadFile = File(...), token: str = Form(...)):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type
    }