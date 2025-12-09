from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, Optional, Literal
from dotenv import load_dotenv
from pydantic import Field, BaseModel

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

#schema
class Review(BaseModel):
    key_themes:list[str] = Field(description = "Write down all key themes discussed in a review in a list")
    summary :str = Field(description = "Brief summary of the review")
    sentiment: Literal["pos","neg"] = Field(description = "Return sentiment of review either negative, positive or neutral")
    pros: Optional[list[str]] = Field(default = None, description = "Write down all pros inside a list")
    cons: Optional[list[str]] = Field(default = None, description ="Write down all cons inside a list")
    name : Optional[str] = Field(default = None, description ="Write name of reviewer")
structured_model = model.with_structured_output(Review)

# Sometime LLM produce correct output for all field w/o mentioning first line in prompt sometimes dont
# Reason LLM only works on prompt we give
# The outptu it give the Langchain parses the text into the dats types mentioned in pydnatic model

"""
1. LangChain wraps the original LLM (model) with a “structured output wrapper.”
2. This wrapper knows about your Pydantic model (Review) and will later:
    Validate the LLM’s output against the model.
    Parse the output into a Python object with the correct fields.
3. Important: The LLM itself (ChatGroq) has no knowledge of the Pydantic model. It doesn’t automatically know to produce key_themes, summary, et
Parse the output into a Python object with the correct fields.

Think of it like a translator sitting between you and the LLM:
    You talk to the LLM (prompt text).
    The LLM responds in plain text.
    The wrapper (LangChain + Pydantic) reads the text and converts it into your structured format.
"""

result = structured_model.invoke("""
Extract the key themes, summary, sentiment, pros, cons from the following product review:
This smartwatch has great health tracking features and the step count is quite accurate. The screen is beautiful and very responsive.
On the downside, the strap feels cheap, and the watch sometimes freezes when switching apps. The battery life is okay, not great.
Review by Ramandeep Kaur
""")

print(result.name)
print(result)
print(type(result))
# print(result['summary'])
# print(result['sentiment'])