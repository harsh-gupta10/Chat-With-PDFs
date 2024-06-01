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

if len(sys.argv) > 2:
    query = sys.argv[1]
    use_vector_embeddings = sys.argv[2] == 'True'
else:
    print("Please provide a query and use_vector_embeddings as command-line arguments.", flush=True)
    sys.exit(1)


if use_vector_embeddings:
    # Use vector embeddings (loaded data)
    NoOfRelaventDoc = 5
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": NoOfRelaventDoc})
    relevant_documents = retriever.get_relevant_documents(query)
    context = ""
    for doc in relevant_documents:
        context += doc.page_content + "\n"
    formatted_prompt = prompt.format(context=context, question=query)
    print('\n\n\n')
    response = model.invoke(formatted_prompt)
else:
    # Use LLM directly
    print('\n\n\n')
    response = model.invoke(query)

chat_history[query] = response
with open(CHAT_HISTORY_FILE, "wb") as f:
    pickle.dump(chat_history, f)

print(response, flush=True)