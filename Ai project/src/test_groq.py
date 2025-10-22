from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print("Loaded key:", api_key[:10] + "..." if api_key else "❌ None found")

try:
    llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=api_key)
    print(llm.invoke("Say hi in one sentence"))
except Exception as e:
    print("⚠️ Error:", e)
