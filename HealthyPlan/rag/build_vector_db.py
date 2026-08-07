from pathlib import Path
import pandas as pd
from .vector_store import embedding_texts, get_chroma_client
from .config import COLLECTION_NAME
Path_Root = Path(__file__).resolve().parents[1]

DATA_PATH = f'{Path_Root}/data/rag/health_knowledge_chunks.csv'
Columns = ['chunk_id','condition_code','content','source_id']
Condition = ["diabetes_type_1", "diabetes_type_2", "diabetes_type_unknown", "prediabetes", "hypertension", "gout", "obesity", "ckd_g1", "ckd_g2", "ckd_g3a", "ckd_g3b", "ckd_g4", "ckd_g5_non_dialysis", "ckd_dialysis", "ckd_stage_unknown", "general_safety"]
def load_data(path):
    try:
        df = pd.read_csv(path,keep_default_na=False,dtype=str)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    return df

def validate_data(df):
    current_columns = df.columns.tolist()

    if current_columns != Columns:
        raise ValueError(f"Invalid columns. Expected: {Columns}, Current: {current_columns}")

    if df.empty:
        raise ValueError("Dataset is empty")

    for column in Columns:
        df[column] = df[column].astype(str).str.strip()
        empty_rows = df[df[column] == ""]

        if not empty_rows.empty:
            raise ValueError(f"Empty values found in column '{column}' at rows: {empty_rows.index.tolist()}")

    print("Columns are valid")
    print("Dataset is not empty")
    print("Empty values: 0")

    return df

def validate_chunk(df):
    duplicate_ids = df[df["chunk_id"].duplicated(keep=False)]

    if not duplicate_ids.empty:
        raise ValueError(f"Duplicate chunk IDs: {duplicate_ids['chunk_id'].tolist()}")

    normalized_content = df["content"].str.lower().str.strip().str.replace(r"\s+", " ", regex=True)
    duplicate_content = df[normalized_content.duplicated(keep=False)]

    if not duplicate_content.empty:
        raise ValueError(f"Duplicate content found:\n{duplicate_content[['chunk_id', 'content']]}")

    invalid_conditions = df[~df["condition_code"].isin(Condition)]

    if not invalid_conditions.empty:
        raise ValueError(f"Invalid condition codes: {invalid_conditions['condition_code'].unique().tolist()}")

    print("Duplicate chunk IDs: 0")
    print("Duplicate content: 0")
    print("Condition codes are valid")

    return df

def embedding_chunk(df):
    contents = df["content"].tolist()
    embeddings = embedding_texts(contents)

    if len(embeddings) != len(df):
        raise ValueError(f"Embedding count {len(embeddings)} does not match chunk count {len(df)}")

    print(f"Embedding shape: {embeddings.shape}")
    return embeddings

def build_vector_store(df, embeddings):
    client = get_chroma_client()
    collection_names = [collection.name for collection in client.list_collections()]

    if COLLECTION_NAME in collection_names:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"Deleted old collection: {COLLECTION_NAME}")

    collection = client.create_collection(name=COLLECTION_NAME, configuration={"hnsw": {"space": "cosine"}})

    ids = df["chunk_id"].tolist()
    documents = df["content"].tolist()
    metadatas = [{"condition_code": row["condition_code"], "source_id": row["source_id"]} for _, row in df.iterrows()]

    collection.add(ids=ids, documents=documents, embeddings=embeddings.tolist(), metadatas=metadatas)

    total_records = collection.count()

    if total_records != len(df):
        raise ValueError(f"Vector store contains {total_records} records but dataset contains {len(df)} chunks")

    print(f"Collection name: {COLLECTION_NAME}")
    print(f"Total records: {total_records}")

    return collection

def main():
    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Validating data...")
    df = validate_data(df)

    print("Validating chunks...")
    df = validate_chunk(df)

    print("Embedding chunks...")
    embeddings = embedding_chunk(df)

    print("Building vector store...")
    collection = build_vector_store(df, embeddings)

    print(f"Total chunks: {len(df)}")
    print(f"Total vectors: {collection.count()}")
    print("Done!")


if __name__ == "__main__":
    
    main()