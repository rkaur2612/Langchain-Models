from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda

load_dotenv()

def word_counter(text):
    return len(text.split())

# function converted to runnable
# runnable_word_counter = RunnableLambda(word_counter)

# since its runnable, it has now invoke function
# result = runnable_word_counter.invoke("How are you?")
# print(result)

prompt= PromptTemplate(
    template ="write a joke about {topic}",
    input_variables = ['topic']
)

# prompt2 = PromptTemplate(
#     template ="explain following joke \n {joke}",
#     input_variables = ['joke']
# )

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

joke_gen_chain = RunnableSequence(prompt, model, parser)

parallel_chain = RunnableParallel(
    {
        'joke': RunnablePassthrough(),
        'word_count':RunnableLambda(word_counter)
    }
)

chain = RunnableSequence(joke_gen_chain,parallel_chain)

result = chain.invoke({'topic':'AI'})

print(result)