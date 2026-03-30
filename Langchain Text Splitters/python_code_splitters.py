from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# This is a STRING. Python will NOT execute this code. 
text = """
class Example:
    def greet(self, name):
        print(f"Hello, {name}!")

    def countdown(self, n):
        if n <= 0:
            print("Done!")
        else:
            print(n)
            self.countdown(n - 1)  # Function calling itself (recursion)


# Create an object of the class
obj = Example()
obj.greet("Alice")
"""

splitter = RecursiveCharacterTextSplitter.from_language(
    language = Language.PYTHON,
    chunk_size = 100, # Small chunk size to force splitting
    chunk_overlap = 0
)

chunks = splitter.split_text(text)

print(f"Total chunks: {len(chunks)}")
print("-" * 20)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}:")
    print(chunk)
    print("-" * 20)
