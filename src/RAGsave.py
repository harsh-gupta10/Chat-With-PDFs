import os
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import sys
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


MODEL = "mistral"
model = Ollama(model=MODEL)
# embeddings = OllamaEmbeddings(model=MODEL)

# ... (rest of your code) ...
loader = PyPDFDirectoryLoader("./data/")

docs_before_split = loader.load_and_split()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 700,
    chunk_overlap  = 50,
)

docs_after_split = text_splitter.split_documents(docs_before_split)


huggingface_embeddings = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",  # alternatively use "sentence-transformers/all-MiniLM-l6-v2" for a light and faster experience.
    model_kwargs={'device':'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
print("Splited The docs")
print("Storing It ......")
vectorstore = FAISS.from_documents(docs_after_split, huggingface_embeddings)
print("Stored Vectors ......")

template = """
Answer the question based on the context below. If you can't
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = PromptTemplate(input_variables=["context", "question"], template=template)




# Check if the query is provided as a command-line argument
if len(sys.argv) > 1:
    query = sys.argv[1]
else:
    print("Please provide a query as a command-line argument.")
    # sys.exit(1)
    query=" "

# ... (rest of your code) ...
relevant_documents = vectorstore.similarity_search(query)
print(f'There are {len(relevant_documents)} documents retrieved which are relevant to the query. Display the first one:\n')
print(relevant_documents[0].page_content)
NoOfRelaventDoc=5
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": NoOfRelaventDoc})
context = ""
for doc in relevant_documents[:NoOfRelaventDoc]:
    context += doc.page_content + "\n"  # Add newline for better readability
formatted_prompt = prompt.format(context=context, question=query)
response = model.invoke(formatted_prompt)
# Instead of print(response), use:
print(response, flush=True)