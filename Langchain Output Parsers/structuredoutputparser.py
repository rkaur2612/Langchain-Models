from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

load_dotenv()

# by default this model can't give structured output
my_llm = HuggingFaceEndpoint(
    repo_id="google/gemma-2-2b-it",
    task="text-generation",
    huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
)

model = ChatHuggingFace(llm=my_llm)

schema = [
    ResponseSchema(name='fact_1', description='Fact 1 about topic'),
    ResponseSchema(name='fact_2', description='Fact 2 about topic'),
    ResponseSchema(name='fact_3', description='Fact 3 about topic')
]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(
    template="Give 3 facts about the {topic} \n {format_instruction}",
    input_variables=['topic'],
    partial_variables={'format_instruction': parser.get_format_instructions()}
)

prompt = template.invoke({'topic':'black hole'})
print(prompt)

result = model.invoke(prompt)

final_result = parser.parse(result.content)

print(final_result)