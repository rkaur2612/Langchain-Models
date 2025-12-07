from langchain_groq import ChatGroq
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt

# Load API key from .env
load_dotenv()

st.header('Research tool')

# creating object of ChatGroq
model = ChatGroq(model="llama-3.1-8b-instant", temperature=0.4, max_tokens=1024) 

paper_input = st.selectbox("Select Research Paper Name", ["Attention Is All You Need", "GPT-3 Language Models are Few-Shot Learners"])

style_input = st.selectbox("Select Explanation Style", ["Beginner friendly", "Technical", "Code Oriented"])

length_input = st.selectbox("Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)"])
# user_input = st.text_input("Enter your prompt")

template = load_prompt('template.json')

# Instead of calling invoke twice call it just once using concept of chain (beloe code - uncommented)
# prompt = template.invoke({
#     'paper_input':paper_input,
#     'style_input':style_input,
#     'length_input':length_input
# })


# if st.button("Summarize"):
#     result = model.invoke(prompt)
#     st.write(result.content)

if st.button("Summaeize"):
    chain = template | model
    result = chain.invoke({
    'paper_input':paper_input,
    'style_input':style_input,
    'length_input':length_input
    })

    st.write(result.content)