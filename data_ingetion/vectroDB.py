from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from openai import OpenAI
import pypdf
import uuid
import os

VECTOR_NAME = "database"
EMBEDDING_MODEL = "togethercomputer/m2-bert-80M-2k-retrieval"

CHROMA_PATH = "./chroma_storage"


api_key = os.getenv("TOGETHER_API")
ai_client = OpenAI(api_key=api_key, base_url="https://api.together.xyz/v1")


def extract_pdf(pdf_path: str) -> str:

    text = ""
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
            text += "\n--PAGE BREAK--\n"

    return text


def create_vectorDB():
    docs_paths = os.listdir(os.getcwd() + "/data_ingetion/firms_report/")

    complete_text = ""

    for doc_path in docs_paths:
        complete_text += extract_pdf(
            os.getcwd() + "/data_ingetion/firms_report/" + doc_path
        )
        complete_text += "\n\n"

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=84,
        length_function=len,
        is_separator_regex=False,
    )

    processed_docs = splitter.split_text(complete_text)
    db_client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = db_client.create_collection(VECTOR_NAME)

    response = ai_client.embeddings.create(input=processed_docs, model=EMBEDDING_MODEL)
    embeddings = [item.embedding for item in response.data]
    unique_ids = [str(uuid.uuid4()) for _ in range(len(embeddings))]
    collection.add(documents=processed_docs, embeddings=embeddings, ids=unique_ids)

    return collection.name


def get_relevant_chunks(query: str):

    db_client = chromadb.PersistentClient(path=CHROMA_PATH)
    found = VECTOR_NAME in [c.name for c in db_client.list_collections()]

    if found:
        collection = db_client.get_collection(VECTOR_NAME)
    else:
        collection = db_client.get_collection(create_vectorDB())

    response = ai_client.embeddings.create(input=query, model=EMBEDDING_MODEL)
    QE = response.data[0].embedding

    relevant_chunks = collection.query(query_embeddings=QE, n_results=4)

    processed = ""

    for idx, doc in enumerate(relevant_chunks["documents"][0], start=1):
        processed += f"Chunks number {idx}\n\n"
        processed += doc + "\n\n"

    return processed
