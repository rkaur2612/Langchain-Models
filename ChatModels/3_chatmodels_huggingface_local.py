from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

#configuring llm
llm = HuggingFacePipeline.from_model_id(
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task ="text-generation",
    pipeline_kwargs={
        "temperature":0.5,
        "max_new_tokens":30
    }
)

# model is an object of ChatHuggingFace
model = ChatHuggingFace(llm=llm)

print("llm object:", llm)
print("llm.pipeline:", getattr(llm, "pipeline", None))
print("type:", type(getattr(llm, "pipeline", None)))

result = model.invoke("What is capital of India")

print(result.content)