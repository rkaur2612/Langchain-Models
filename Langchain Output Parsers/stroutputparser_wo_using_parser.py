# EXAMPLE - W/O USING OUTPUT PARSER

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
#dyanamic prompts
from langchain_core.prompts import PromptTemplate

load_dotenv()

# by default this model can't give structured output
my_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-4B-Thinking-2507",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)

# chat model
model = ChatHuggingFace(llm=my_llm)

# 1st prompt - detailed report
template1 = PromptTemplate(
    template = 'Write a detailed report on {topic}',
    input_variables= ['topic']
)

# 2nd prompt - summary
template2 = PromptTemplate(
    template = 'Write a 5 line summary on the following text. /n {text}',
    input_variables= ['text']
)

# send topic to template 1 and save as prompt1
prompt1 = template1.invoke({'topic':'black hole'})
# print("prompt1:", prompt1)

# send prompt1 to model and save result 
result = model.invoke(prompt1)
# print("result:", result)

# send result.content as text to template2 and save as prompt2
prompt2 = template2.invoke({'text':result.content})
# print("prompt2:", prompt2)

# send prompt2 to model -> save as result1
result1 = model.invoke(prompt2)

print(result1.content)
