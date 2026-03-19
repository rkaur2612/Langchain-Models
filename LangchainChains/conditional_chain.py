"""
# USE CASE

-> user send feedback on e-commerce app 
-> model analyse sentiment and classify as positive/negative
-> if positive, send appropriate reply back to user
-> if negative, send appropriate reply back to user

"""

from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field, ValidationError

# RunnableLambda - converts lambda function in runnable
# RunnableParallel - parallely run multiple chains
# RunnableBranch - run conditional chains
from langchain_core.runnables import RunnableParallel, RunnableBranch, RunnableLambda
from typing import Literal

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")
parser1 = StrOutputParser()

class Feedback(BaseModel):
    sentiment : Literal['positive','negative'] = Field(description = "Give the sentiment of the feedback")

parser2 = PydanticOutputParser(pydantic_object=Feedback)

prompt1 = PromptTemplate(
    template ="Classify the sentiment of following feedback text into positive or negative.\n {feedback} \n {format_instructions}",
    input_variables = ['feedback'],
    partial_variables = {'format_instructions' : parser2.get_format_instructions()}
)

prompt2 = PromptTemplate(
    template ="Write an appropriate response to this positive feedback \n {feedback}",
    input_variables = ['feedback']
)

prompt3 = PromptTemplate(
    template ="Write an appropriate response to this negative feedback \n {feedback}",
    input_variables = ['feedback']
)

classifier_chain = prompt1 | model | parser2

# x is : sentiment ='negative' or sentiment ='positive
# value returned by classifier chain
# why we did x.sentiment as x is pydantic object (so we are accessing value of its attribute)
branch_chain = RunnableBranch(
    (lambda x:x.sentiment == 'positive', prompt2 | model | parser1), # if x.sentiment = positive execute this chain
    (lambda x:x.sentiment == 'negative', prompt3 | model | parser1), # if x.sentiment = negativet execute this chain
    RunnableLambda(lambda x:"could not find sentiment") # default chain
)

chain = classifier_chain | branch_chain

text = "This is a wonderful smartwatch"

# result = classifier_chain.invoke({'feedback': text}).sentiment
result = chain.invoke({'feedback': text})

print(result)

# visualise chain
chain.get_graph().print_ascii()