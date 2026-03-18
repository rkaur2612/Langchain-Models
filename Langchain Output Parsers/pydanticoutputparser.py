from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant") 

# by default this model can't give structured output
# my_llm = HuggingFaceEndpoint(
#     repo_id="google/gemma-2-2b-it",
#     task="text-generation",
#     huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
# )

model = llm

class Facts(BaseModel):
    fact_1: str = Field(description="Fact 1 about topic")
    fact_2: str = Field(description="Fact 2 about topic")
    fact_3: str = Field(description="Fact 3 about topic")

parser = PydanticOutputParser(pydantic_object=Facts)

# while forming prompt we send additional instruction that tells which format output is required
template = PromptTemplate(
    template="Give 3 facts about the {topic}. \n {format_instructions}",
    input_variables=['topic'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

# in place of below four sentence we can use concept of chains - below
prompt = template.invoke({'topic':'India'})
print("prompt\n",prompt)
print()

result = model.invoke(prompt)
print("result\n",result)
print()

try:
    final_result = parser.parse(result.content)
    print("final_result\n",final_result)
    print()

    print(type(final_result))

except ValidationError as ve:
    print("❌ Validation Error:", ve)

except Exception as e:
    print("❌ Parsing Failed:", e)


# chain = template | model | parser

# result = chain.invoke({'topic': 'Pandas'})
# print(result)
# print(type(result))