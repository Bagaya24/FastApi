from fastapi import FastAPI, BackgroundTasks, Depends
import time

"""
Dans cette partie, nous avons vu que l'on peut faire certaine requete sans pour autant imformer a utilisateur que nous
l'avons fait, ca peut etre juste un processuss fait en arriere plan, pour se faire, nous avons utilise BackgroundTasks.
Ca permet juste d'excecuter une fonction en arriere plan
"""

app = FastAPI()

# def write_notification(email: str, message=""):
#     with open("log.txt", mode="w") as email_file:
#         content = f"notification for {email}: {message}"
#         time.sleep(5)
#         email_file.write(content)
#
# @app.post("/send-notification-email/{email}", status_code=202)
# async def send_notification(email: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(write_notification, email, message="some notification")
#     return {"message": "Notification sent in the background"}

def write_log(message: str):
    with open("log.txt", mode="a") as log_file:
        log_file.write(message)

def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q

@app.post("/send-notification-log/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)):
    message = f"notification for {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Notification sent in the background"}