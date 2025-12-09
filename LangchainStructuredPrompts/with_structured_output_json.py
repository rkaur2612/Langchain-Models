from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, Optional, Literal
from dotenv import load_dotenv
from pydantic import Field, BaseModel

load_dotenv()

model = ChatGroq(model="llama-3.1-8b-instant")

#schema
json_object = {
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Write down all key themes discussed in a review in a list"
    },
    "summary": {
      "type": "string",
      "description": "Brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["pos", "neg"],
      "description": "Return sentiment of review either negative, positive or neutral"
    },
    "pros": {
      "type": ["array", "null"],
      "items": { "type": "string" },
      "description": "Write down all pros inside a list"
    },
    "cons": {
      "type": ["array", "null"],
      "items": { "type": "string" },
      "description": "Write down all cons inside a list"
    },
    "name": {
      "type": ["string", "null"],
      "description": "Write name of reviewer"
    }
  },
  "required": ["key_themes", "summary", "sentiment"]
}


structured_model = model.with_structured_output(json_object)

result = structured_model.invoke("""
This smartwatch has great health tracking features and the step count is quite accurate. The screen is beautiful and very responsive.
On the downside, the strap feels cheap, and the watch sometimes freezes when switching apps. The battery life is okay, not great.
Review by Ramandeep Kaur
""")

print(result)
# print(type(result))
# print(result['summary'])
# print(result['sentiment'])