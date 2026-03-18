from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

my_llm = ChatGroq(model="llama-3.1-8b-instant") 

# by default this model can't give structured output
# my_llm = HuggingFaceEndpoint(
#     repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
#     task="text-generation",
#     huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
# )

model = my_llm

parser = JsonOutputParser()

# while forming prompt we send additional instruction that tells which format output is required
template = PromptTemplate(
    template="Give me name, age and city of fictional person \n {format_instruction}",
    input_variables=[],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

# in place of below four sentence we can use concept of chains - below
# prompt = template.format()

# print(prompt)

# result = model.invoke(prompt)

# final_result = parser.parse(result.content)

# print(final_result)

# print(type(final_result))

chain = template | model | parser

result = chain.invoke({})
print(result)
print(type(result))