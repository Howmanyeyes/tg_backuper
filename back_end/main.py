"""Main module for running everything"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from config import config
from utils import backend_answer, log_this
app = FastAPI()
app.mount("/static", StaticFiles(directory="front_end"), name="static")
templates = Jinja2Templates(directory=".")

@app.get("/")
async def main_page(request : Request):
    """Main page with all settings and buttons"""
    return  templates.TemplateResponse("front_end/index.html", {"request": request})




@app.get("/api/get_settings/")
@log_this
@backend_answer
async def return_settings():
    """Returns saved settings to front"""
    return config.export('json')

@app.post("/api/save_settings/")
async def save_settings(request : Request):
    """Saves settings to file"""
    data = await request.json()
    config.edit_dict(data, 'dict')


if __name__ == "__main__":

    uvicorn.run("main:app", host="localhost", port=9112, reload=True)
