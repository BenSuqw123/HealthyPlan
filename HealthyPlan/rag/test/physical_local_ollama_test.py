import sys

from rag_pipeline import run_rag_pipeline


def test_physical_local_ollama():
    query = "Tôi bị béo phì và tiểu đường type 2, nên giảm cân thế nào?"

    print("================================================================================")
    print("PHYSICAL LOCAL OLLAMA TEST")
    print("================================================================================")
    print(f"Query: {query}")

    try:
        pipeline_result = run_rag_pipeline(
            query=query,
            top_n=3,
        )

        print(f"Primary Route: {pipeline_result['primary_route']}")
        print(f"Conditions: {pipeline_result['conditions']}")
        print(f"Safety Flags: {pipeline_result['safety_flags']}")
        print(f"Retrieved Chunk Count: {pipeline_result['retrieved_chunk_count']}")
        print(f"Context Source Count: {pipeline_result['context_data']['source_count']}")
        print("--------------------------------------------------------------------------------")
        print("Generated Answer:")
        print(pipeline_result["answer"])
        print("================================================================================")

    except Exception as error:
        print("Ollama local service status: Offline / Not running on http://localhost:11434")
        print(f"Details: {error}")
        print("================================================================================")


if __name__ == "__main__":
    test_physical_local_ollama()
