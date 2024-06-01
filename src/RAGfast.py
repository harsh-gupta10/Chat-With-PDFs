import os
import pickle
import hashlib
from langchain_community.llms import Ollama
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys

MODEL = "mistral"
model = Ollama(model=MODEL)

VECTORSTORE_FILE = "vectorstore.pkl"
CHAT_HISTORY_FILE = "chat_history.pkl"
# DATA_DIR_HASH_FILE = "data_dir_hash.pkl"

def get_data_dir_hash(directory):
    file_hashes = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "rb") as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            file_hashes.append(file_hash)
    return hash(tuple(sorted(file_hashes)))


# data_dir_hash_current = get_data_dir_hash("./data/")
# data_dir_hash = None


try:
    with open(VECTORSTORE_FILE, "rb") as f:
        vectorstore = pickle.load(f)
        print("Loaded vectorstore from file.")
except FileNotFoundError:
    print("Vectorstore file not found. Creating a new one.")
    loader = PyPDFDirectoryLoader("./data/")
    docs_before_split = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=50,
    )
    docs_after_split = text_splitter.split_documents(docs_before_split)

    huggingface_embeddings = HuggingFaceBgeEmbeddings(
        model_name="BAAI/bge-small-en-v1.5",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    print("Splited The docs")
    print("Storing It ......")
    vectorstore = FAISS.from_documents(docs_after_split, huggingface_embeddings)
    print("Stored Vectors ......")
    with open(VECTORSTORE_FILE, "wb") as f:
        pickle.dump(vectorstore, f)
    # with open(DATA_DIR_HASH_FILE, "wb") as f:
    #     pickle.dump(data_dir_hash_current, f)
    # data_dir_hash = data_dir_hash_current

    # vectorstore.metadata["data_dir_hash"] = data_dir_hash

# try:
#     with open(DATA_DIR_HASH_FILE, "rb") as f:
#         data_dir_hash = pickle.load(f)
#         print("Loaded data directory hash from file.")
# except FileNotFoundError:
#     print("Data directory hash file not found.")
#     data_dir_hash = None
    

# if data_dir_hash_current != data_dir_hash:
#     print("Data directory has changed. Recreating the vectorstore.")
#     loader = PyPDFDirectoryLoader("./data/")
#     docs_before_split = loader.load_and_split()
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=700,
#         chunk_overlap=50,
#     )
#     docs_after_split = text_splitter.split_documents(docs_before_split)
#     huggingface_embeddings = HuggingFaceBgeEmbeddings(
#         model_name="BAAI/bge-small-en-v1.5",
#         model_kwargs={'device': 'cpu'},
#         encode_kwargs={'normalize_embeddings': True}
#     )
#     vectorstore = FAISS.from_documents(docs_after_split, huggingface_embeddings)
#     with open(VECTORSTORE_FILE, "wb") as f:
#         pickle.dump(vectorstore, f)
#     with open(DATA_DIR_HASH_FILE, "wb") as f:
#         pickle.dump(data_dir_hash_current, f)


template = """
Answer the question based on the context below. If you can't
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)

try:
    with open(CHAT_HISTORY_FILE, "rb") as f:
        chat_history = pickle.load(f)
        print("Loaded chat history from file.")
except FileNotFoundError:
    print("Chat history file not found. Creating a new one.")
    chat_history = {}


# Check if the query is provided as a command-line argument
if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    print("Please provide a query as a command-line argument.")
    query = " "

NoOfRelaventDoc = 5
relevant_documents = vectorstore.similarity_search(query)
context = ""
for doc in relevant_documents[:NoOfRelaventDoc]:
    context += doc.page_content + "\n"

# Include chat history in the prompt
chat_history[query] = ""
for q, a in chat_history.items():
    context += f"Human: {q}\nAssistant: {a}\n"

formatted_prompt = prompt.format(context=context, question=query)
print("Genrating from LLM.....")
response = model.invoke(formatted_prompt)
chat_history[query] = response
with open(CHAT_HISTORY_FILE, "wb") as f:
    pickle.dump(chat_history, f)

print(response, flush=True)