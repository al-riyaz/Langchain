from langchain_google_genai import ChatGoogleGenerativeAI
from keys import get_api_key

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=get_api_key())
response = llm.invoke("Who is Mahatma Gandhi")
print(response.content)
