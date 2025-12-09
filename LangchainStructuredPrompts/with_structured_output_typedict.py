from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, Optional, Literal
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

#schema
class Review(TypedDict):
    key_themes:Annotated[list[str], "Write down all key themes discussed in a review in a list"]
    summary: Annotated[str, "Brief summary of review"]
    sentiment: Annotated[Literal["pos","neg"], "Return sentiment of review either negative, positive or neutral"]
    pros: Annotated[Optional[list[str]], "Write down all pros inside a list"]
    cons: Annotated[Optional[list[str]], "Write down all cons inside a list"]

structured_model = model.with_structured_output(Review)

result = structured_model.invoke("""
Extract the ket themes, summary, sentiment, pros and cons from the following product review:
This smartwatch has great health tracking features and the step count is quite accurate. The screen is beautiful and very responsive.
On the downside, the strap feels cheap, and the watch sometimes freezes when switching apps. The battery life is okay, not great.
""")

print(result)
# print(type(result))
# print(result['summary'])
# print(result['sentiment'])