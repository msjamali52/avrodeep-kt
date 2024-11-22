from app.modules.vectorDB.crud import vectorDB_crud
from app.modules.ai.engine import OpenAI_Engine
from app.modules.ai.prompts import *
import json

with open('project3.json', 'r') as file:
    data = json.load(file)

# vectorDB_crud().add_data("risks_embed_2", data["projects"])

query = "I want to construct a garage? what are the risks?"

fetch_records = vectorDB_crud().get_query_similarity("risks_embed_3", query, 15, 0.45)

fetched_records = [project for project in data["projects"] if str(project["id"]) in fetch_records["ids"][0]]

reranked = OpenAI_Engine().generate(filter_rows.format(project_rows = fetched_records), query)

generate_response = OpenAI_Engine().generate(summarize_risks.format(project_rows = reranked), query)

print(generate_response)

# for i in fetched_records:
#     print(i["id"], i["name"])
# print("-------------")
# for i in reranked["filtered_rows"]:
#     print(i["id"], i["name"],"\n--->Reason:\n", i["reason"])
