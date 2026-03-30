from langchain_text_splitters import RecursiveCharacterTextSplitter

text ="""
My name is Raman
I live in gurgaon

I am 30 years old
How are you"""

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 25,
    chunk_overlap = 0
)

result = splitter.split_text(text)

print(result)