from app.modules.vectorDB.crud import vectorDB_crud
from app.modules.ai.prompts import *
import json

with open('project3.json', 'r') as file:
    data = json.load(file)

vectorDB_crud().add_data("risks_embed_3", data["projects"])