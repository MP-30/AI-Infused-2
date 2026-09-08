# from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from scraper import fetch_website_contents   # reuse Class 1's scraper

load_dotenv()

prompt = ChatPromptTemplate.from_template(            # ①
    "Give a short, friendly summary of this website:\n\n{website}")

model  = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
parser = StrOutputParser()

chain = prompt | model | parser

def summarize(url):
    return chain.invoke({"website": fetch_website_contents(url)})   # ⑤

print(summarize("https://anthropic.com"))