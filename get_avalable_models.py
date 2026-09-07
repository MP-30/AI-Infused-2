import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

gemini_client = OpenAI(api_key=os.getenv("GEMINI_API_KEY"),
                            base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

models = client.models.list()
for model in models.data:
    print(model.id)
print('***************************')
print('Gemini')
print('***************************')
models1 = gemini_client.models.list()
for model1 in models1.data:
    print(model1.id)