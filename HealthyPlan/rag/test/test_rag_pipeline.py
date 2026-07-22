from rag_pipeline import run_rag_retrieval


query = "Tôi bị béo phì và tiểu đường type 2, nên giảm cân thế nào?"

result = run_rag_retrieval(
    query=query,
    top_n=3,
)

print("Primary route:", result["condition_code"])
print("Conditions:", result["conditions"])
print("Retrieval conditions:", result["retrieval_condition_codes"])
print("Safety flags:", result["safety_flags"])
print("Retrieved chunks:", result["retrieved_chunk_count"])

for chunk in result["retrieved_chunks"]:
    print(
        chunk["rank"],
        chunk["condition_code"],
        chunk["similarity"],
        chunk["content"],
    )