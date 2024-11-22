from app.modules.vectorDB.crud import vectorDB_crud
from app.modules.ai.engine import OpenAI_Engine
from app.modules.ai.prompts import *
import json

with open('project3.json', 'r') as file:
    data = json.load(file)

chat_history = []

def query(query: str,  document_name : str = "risks_embed_3", limit:int = 15, threshold: int = 0.45):
    global chat_history
    fetch_records = vectorDB_crud().get_query_similarity(document_name, query, limit, threshold)
    fetched_records = [project for project in data["projects"] if str(project["id"]) in fetch_records["ids"][0]]

    reranked = OpenAI_Engine().generate(filter_rows.format(project_rows = fetched_records), query)

    if chat_history:
        chat_history_fetch = chat_history[-4:]
    else: chat_history_fetch = []
    print(f"----------{chat_history_fetch}-----{chat_history}-----")
    generate_response = OpenAI_Engine().generate(summarize_risks.format(project_rows = reranked, chat_history = chat_history_fetch), query)

    chat_history.append({"user": query})
    chat_history.append({"bot" : generate_response})

    return json.loads(generate_response)["response"]

    
