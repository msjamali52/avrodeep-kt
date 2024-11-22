from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class OpenAI_Engine:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
    def generate(self, prompt, messages):
        final_output = client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": prompt}, 
                {"role": "user", "content": messages}
                ]
        )
        return final_output.choices[0].message.content