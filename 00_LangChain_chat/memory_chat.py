import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


model = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly tutor."),     # ① personality, like Class 1
    MessagesPlaceholder("history"),              # ② past turns park here
    ("human", "{question}"),                     # ③ the new question
])
chain = prompt | model

history = []

print("Chat with the bot (type 'quit' to exit).")
while True:
    question = input("You: ")
    if question.strip().lower() in {"quit", "exit"}:
        break
    answer = chain.invoke(
        {"history": history, "question": question}
    ).content
    print("Bot:", answer)
    history.append(HumanMessage(question))
    history.append(AIMessage(answer))
    print(f" (history now has {len(history)} message)")