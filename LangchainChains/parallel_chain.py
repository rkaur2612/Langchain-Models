"""
# USE CASE

user -> topic -> LLM -> generated detailed report -> LLM -> extract summary -> o/p

"""

from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# runnable using which we can parallely run multiple chains
from langchain_core.runnables import RunnableParallel

load_dotenv()

prompt1 = PromptTemplate(
    template ="Generate short and simple notes from following text \n {text}",
    input_variables = ['text']
)

prompt2 = PromptTemplate(
    template ="Generate 5 short question answer from the following text \n {text}",
    input_variables = ['text']
)

prompt3 = PromptTemplate(
    template ="Merge the provided notes and quiz into a single document \n {notes} and {quiz}",
    input_variables = ['notes','quiz']
)

model = ChatGroq(model="llama-3.1-8b-instant")

parser = StrOutputParser()

parallel_chain = RunnableParallel({
    'notes': prompt1 | model | parser,
    'quiz' : prompt2 | model | parser
})

merge_chain = prompt3 | model | parser

chain = parallel_chain | merge_chain

text = "Gradient Descent is an iterative optimization algorithm used to minimize a cost function by adjusting model parameters in the direction of the steepest descent of the function’s gradient. In simple terms, it finds the optimal values of weights and biases by gradually reducing the error between predicted and actual outputs.Suppose youre at the top of a hill and your goal is to find the lowest point in the valley. You can't see the entire valley from the top, but you can feel the slope under your feet. Start at the Top: You begin at the top of the hill (this is like starting with random guesses for the model's parameters).Feel the Slope: You look around to find out which direction the ground is sloping down. This is like calculating the gradient, which tells you the steepest way downhill.Take a Step Down: Move in the direction where the slope is steepest (this is adjusting the model's parameters). The bigger the slope, the bigger the step you take. Repeat: You keep repeating the process feeling the slope and moving downhill until you reach the bottom of the valley (this is when the model has learned and minimized the error). What is Learning Rate?Learning rate is a important hyperparameter in gradient descent that controls how big or small the steps should be when going downwards in gradient for updating models parameters. It is essential to determines how quickly or slowly the algorithm converges toward minimum of cost function.1. If Learning rate is too small: The algorithm will take tiny steps during iteration and converge very slowly. This can significantly increases training time and computational cost especially for large datasets."

result = chain.invoke({'text': text})

print(result)

# visualise chain
chain.get_graph().print_ascii()