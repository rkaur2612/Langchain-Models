from langchain_core.prompts import PromptTemplate

#template
# Prompt templates class helps to create dynamic messages
# Used only in single turn messages
template = PromptTemplate(
    template="""
    Please summarise research paper titled "{paper_input}" with the following specifications:
    Explanation Style: {style_input}
    Explanation Length: {length_input}
    1. Mathematical Details:
      - Include relevant mathematical equations if present in paper.
      - Explain mathematical concepts using simple, intuitive code snippets where applicable
    2. Analogies:
      - Use relatable analogies to simplify complex ideas.
    If certain information is not available in paper, responsd with: "Insufficient information available" instaed 
    of guessing.
    Ensure the summary is clear , accurate, and aligned with provided style and length,
    input""",
    input_variables =["paper_input", "style_input", "length_input"],
    validate_template = True
)

template.save('template.json')