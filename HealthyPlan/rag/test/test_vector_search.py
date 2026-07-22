from retriever import retrieve


def main():
    query = "Người bị gout nên hạn chế thực phẩm nào?"
    results = retrieve(query, top_n=5, condition_code="gout")

    print(f"Query: {query}")
    print(f"Total results: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Condition: {result['condition_code']}")
        print(f"Source: {result['source_id']}")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Similarity: {result['similarity']:.4f}")
        print(f"Content: {result['content']}")


if __name__ == "__main__":
    main()