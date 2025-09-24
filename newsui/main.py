from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# MongoDB connection
mongo_uri = os.environ.get("MONGODB_CONNECTIONSTRING")
client = MongoClient(mongo_uri, server_api=ServerApi('1'))
db = client.get_database("newsdb")
collection = db.get_collection("articles")

@app.get("/", response_class=HTMLResponse)
async def read_articles(request: Request):
    articles = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB _id field
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})
