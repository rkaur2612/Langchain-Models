from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda, RunnableBranch

load_dotenv()

prompt1 = PromptTemplate(
    template ="write a detailed report on {topic}",
    input_variables = ['topic']
)

prompt2 = PromptTemplate(
    template ="Summarise following text \n {text}",
    input_variables = ['text']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

report_gen_chain = RunnableSequence(prompt1, model, parser)

branch_chain = RunnableBranch(
            (   # x is output from parser from report_gen_chain as those will be connected later
                # if x is > 500 then run this runnable sequence to genearte summary
                lambda x : len(x.split()) > 300, RunnableSequence(prompt2, model, parser)), 
            (RunnablePassthrough()) # if x < 500 then simple print parser o/p
)


chain = RunnableSequence(report_gen_chain,branch_chain)

result = chain.invoke({'topic':'AI'})

print(result)