import os
from dotenv import load_dotenv


os.environ["HF_HOME"] = "E:/study/AIP_capstone/capstone/models/hf_cache"
os.environ["TRANSFORMERS_CACHE"] = "E:/study/AIP_capstone/capstone/models/hf_cache"


import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface import HuggingFaceLLM
from src.workflow import FoodRecommendationWorkflow
from huggingface_hub import login


load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
login(token=HF_TOKEN)


def load_llm(model_name_or_path: str):
    """Load HuggingFace model for LlamaIndex."""
    return HuggingFaceLLM(
        model_name=model_name_or_path,
        tokenizer_name=model_name_or_path,
        context_window=4096,
        max_new_tokens=512,
        generate_kwargs={"temperature": 0.7, "do_sample": True},
        device_map="cuda",
    )


def setup_workflow(
    model_name_or_path: str,
    db_path: str = "E:\\study\\AIP_capstone\\capstone\\data\\UserPreference_chroma_db_MiniLM-L12-v2",
    collection_name: str = "UserPreference_collection",
    threshold: float = 0.5,
):
    """
    Thiết lập workflow cho FoodRecommendation system.

    Args:
        model_name_or_path (str): Đường dẫn đến model HF (merge hoặc base+LoRA).
        db_path (str): Đường dẫn tới thư mục ChromaDB local.
        collection_name (str): Tên collection trong DB.
        threshold (float): Ngưỡng dùng cho Recommendation Agent.

    Returns:
        FoodRecommendationWorkflow instance.
    """

    # 1. Kiểm tra / khởi tạo client ChromaDB
    os.makedirs(db_path, exist_ok=True)
    client = chromadb.PersistentClient(path=db_path)

    # 2. Lấy hoặc tạo collection
    collection = client.get_or_create_collection(collection_name)

    # Debug info
    print(f"Connected to ChromaDB: {db_path}")
    print(f"Collection: {collection_name}")
    try:
        print(f"Current vectors: {collection.count()}")
    except Exception:
        print("!Could not count vectors (maybe empty collection)")

    # 3. Tạo VectorStore và Embedding model
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2" # Thay đổi embedding model
    )
    vector_store = ChromaVectorStore(chroma_collection=collection)

    # 4. Build VectorStoreIndex
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)
    retriever = index.as_retriever(similarity_top_k=10)

    # 5. Load LLM (merged hoặc adapter)
    llm = load_llm(model_name_or_path)

    # 6. Kết hợp thành workflow
    workflow = FoodRecommendationWorkflow(llm, index, retriever, threshold=threshold)
    print("Workflow setup complete!")

    return workflow
