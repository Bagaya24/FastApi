from datetime import datetime, timedelta, time

from fastapi import FastAPI
from uuid import UUID

from fastapi.params import Body

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items(item_id: UUID,
                     start_date: datetime | None = Body(None),
                     en_date: datetime | None = Body(None),
                     repeat_time: time | None = Body(None),
                     process_after: timedelta | None = Body(None)):
    start_process = start_date - process_after
    duration = en_date - start_date
    return {"item_id": item_id, "start_date": start_date, "en_date": en_date, "repeat_at": repeat_time, "start_process": start_process, "duration": duration}
