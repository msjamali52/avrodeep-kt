filter_rows = """From the following list of rows from a database, select only those rows which may have similar risks associated with the risk of the task as given by the user query:
{project_rows}

Return a JSON with the 'filtered_rows' key, having only the revlevant rows. DO NOT miss, modify any details from the rows choosen.
Also include a 'reason' of why that row was selected
"""

summarize_risks = """You are given the following rows from a database that contains risks associated with each project:
{project_rows} #List[dict] where each dict is a project row

Use the following conversation history between you(bot) and user to understand the context:
{chat_history}

Your task is to inform the user about the risks associated with the task given in the user query that would include:
1. Risks from previous same projects from the list given.
2. Risks from the unrelated projects but may have similar risks. If choosen, include how the risk will be related to the query.
3. Any risks other than the above that you may know can happen.

Instructions:
1. For each risk that is referenced from the list provided, only include the date and id, so that the user can relate. 
2. If user_query has the specific project id that is present in the list, you must include all the summary of the details it along with the risks.
3. Do not modify, add your own information if referencing from the list provided.
4. All the responses should be in Natural language.

Return a json having your response in the 'response' key.
"""