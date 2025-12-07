# Static prompt with saved chat history
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

# creating object of ChatGroq
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.4, max_tokens=1024) 

chat_history = [
    SystemMessage(content = "You are a helpful AI Assistant")
]

while True:
    user_input = input('You: ')
    chat_history.append(HumanMessage(content = user_input))
    if user_input == 'exit':
        break
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content = result.content))
    print("AI: ", result.content)

print(chat_history)
