# when we use parser , it automatically extract content from llm result 
# so we dont have to do result.content

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# by default this model can't give structured output
my_llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen3-4B-Thinking-2507",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)

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

parser = StrOutputParser()

# parser will extract just content from full result (which contains meta data)
chain = template1 | model | parser | template2 | model | parser

result = chain.invoke({'topic': 'black hole'})

print(result)