from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough

load_dotenv()

prompt1= PromptTemplate(
    template ="write a joke about {topic}",
    input_variables = ['topic']
)

prompt2 = PromptTemplate(
    template ="explain following joke \n {joke}",
    input_variables = ['joke']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

joke_gen_chain = RunnableSequence(prompt1, model, parser)

parallel_chain = RunnableParallel(
    {
        'joke': RunnablePassthrough(),
        'joke_explaination': RunnableSequence(prompt2,model,parser),
    }
)

chain = RunnableSequence(joke_gen_chain,parallel_chain)

result = chain.invoke({'topic':'AI'})

print(result)
