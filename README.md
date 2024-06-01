# Chat with PDF

This project is a web application that allows users to have natural language conversations with the information contained in PDF files. It combines the power of large language models and vector embeddings to provide relevant and contextual responses based on the user's queries. We use the RAG (Retrieval Augmented Generation) approach.

## Problem Statement

Accessing and understanding information from large PDF documents can be a time-consuming and tedious task. This project aims to solve this problem by providing a conversational interface where users can ask questions related to the content of the PDF files, and the application will provide relevant and contextual responses based on the information contained in the documents.

If you're a business owner, you can use this application to create a custom chatbot that replies to user queries based on your own data. For example, an airline company can create a chatbot with information about all the services offered, flight details, and various processes related to the airline.

One of the major advantages of the RAG approach is that it provides results related to your business data only. For instance, if you feed the Indian constitution into the system and ask it to write a Python code, it will not generate that code. Similarly, if you feed it with a Data Structures and Algorithms book and ask a question about the capital of India, it may not answer or will say it's out of context.

We are using open-source large language models (LLMs), embeddings, and vector storage. There is no involvement of any API keys, so it runs locally on the respective machine for data privacy (not using any third-party API). I have downloaded the Mistral 7B model from Ollama and installed it. It might take some time as we are doing everything locally. The time depends on the specifications of the machine. (On my machine, a Ryzen 3 5300U with integrated GPU, it usually takes around 3 minutes for each query, and to store a new 4.4MB PDF document, it takes around 4 minutes.)

## Features

- **Load PDF files**: The application can load and process multiple PDF files, allowing users to query information from a collection of documents.
- **Natural Language Processing**: Users can ask questions in natural language, and the application will understand and process the queries using advanced language models.
- **Vector Embeddings**: The application uses vector embeddings to represent the content of the PDF files, enabling efficient similarity search and retrieval of relevant information.
- **Context-aware Responses**: When using vector embeddings, the application provides responses based on the relevant context from the PDF files, ensuring that the responses are accurate and coherent.
- **Direct Language Model Responses**: Users can choose to bypass the vector embeddings (loaded documents) and receive direct responses from the large language model, allowing for more open-ended responses, including responses that are not related to the topic.

## Concepts and Technologies Used

- **React.js**: The frontend of the application is built using React.js, a popular JavaScript library for building user interfaces.
- **Flask**: The backend server is implemented using the Flask web framework, which handles HTTP requests and responses.
- **LangChain**: The project utilizes LangChain, a framework for building applications with large language models, for processing natural language queries and generating responses.
- **Ollama**: Ollama, an open-source language model, is used as the primary language model for generating responses.
- **FAISS**: FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors, used for vector embeddings and similarity search in this project.
- **HuggingFace Embeddings**: The application uses HuggingFace's pre-trained embeddings for representing the text content of the PDF files as dense vectors.
- **WebSockets**: WebSockets are used for real-time communication between the frontend and backend, enabling seamless updates and responses.

## Requirements and Dependencies

### Backend

- Python 3.7 or later
- LangChain
- Ollama
- FAISS
- Flask
- Pickle
- HuggingFaceBgeEmbeddings
- mistral 7B

### Frontend

- Node.js
- React.js
- Axios
- Socket.io-client
- React-Markdown
- react-code-blocks

## Directory Structure

- All important files are in the `src` folder.
- Inside the `src` folder:
 - `data` -> This directory stores all PDF files containing business data.
 - `chatInterfaceSave.js` contains the UI of the application.
 - `fakeRAG.py` is used to test the RAG integration with the UI. As the correct UI takes 2-3 minutes per query, the fake file doesn't invoke the query and returns a fixed answer.
 - `MarkdownRenderer.js` is used to display the markdown language output from the LLM correctly, using the `react-markdown` library.
 - `MdContent.js` is a testing file to test the `react-markdown` library (it has a dummy response from the LLM).
 - `server.py` is the Flask server file.
 - `RAGandLLM` is the main RAG file (final iteration). Other files related to RAG are previous iterations.
 - `workingRAG.ipynb` is a Jupyter Notebook containing the implemented RAG.

## Installation and Setup

1. Clone the repository: `git clone https://github.com/your-repo.git`
2. Run `curl -fsSL https://ollama.com/install.sh | sh` on Linux to download Ollama.
3. Install the [Mistral 7B](https://ollama.com/library/mistral) model by running `ollama run mistral` in the terminal (also check if it's running or not).
4. Install other required dependencies.
5. Start the frontend development server: `npm start` (inside the repository).
6. Start the backend development server: `flask --app server run` (in the `src` folder).
7. Open your web browser and navigate to `http://localhost:3000` to access the application.

## Usage

1. Currently, there is no option to upload PDFs. Please put the PDF files in the `./src/data` directory. The code will read files from there. (For now, I have kept a Data Structures and Algorithms book there, `DataStructures.pdf`). If you're changing anything in `./src/data`, delete the previous `vectorstore.pkl` file so that it will delete the previously stored data and store the new data (if not deleted, it will think the data is unchanged).
2. Enter your question or query in the chat input field. (It will take some time, approximately 2-3 minutes, to generate the results, depending on the specifications (GPU) of your machine and the query, as we are using it completely offline).
3. There is a checkbox to choose whether you want to use vector embeddings (loaded data/PDFs) for context-aware responses or get direct responses from the large language model. Even if it is checked out it has the context of previous chats. It Just switches it from RAG to LLM and LLM to RAG. To delete Chat context Read point 6.
4. Click the "Submit" button or press Enter to send your query.
5. The application will process your query and display the response in the chat window.
6. If the context of chat has Become Non relevant then Delete the `chat_history.pkl` file. and Start the conversation.
   

## Further Work

- **Improved User Interface**: The current user interface is basic and can be enhanced to provide a better user experience, including features like file upload, chat history navigation, and more.
- **Multilingual Support**: Currently, the application supports only English language queries and responses. Adding support for multiple languages would increase its usability and reach.
- **Performance Optimizations**: As the number of PDF files and chat sessions grows, performance optimizations may be required.
- **Advanced Query Processing**: Implementing advanced query processing techniques, such as query rewriting or query expansion, could improve the relevance and accuracy of the responses.
- **Integration with Cloud Services**: The application could be integrated with cloud services for storage, processing, and scalability, enabling easier deployment and better resource management.
- **Use of Better Machines, LLMs, Embedding Models**: Using better hardware resources, more powerful LLMs, and improved embedding models could enhance the performance and accuracy of the application.
- **UI Improvements**: The current UI loses chat history (while context is being stored), and user authentication could be added.
- **Support for Different File Types and Links**: Enabling the application to process different file types and web links in addition to PDFs would increase its versatility.

## Contributing

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.




## Acknowledgments

- [LangChain](https://github.com/hwchase17/langchain) for the framework and tools for building applications with large language models.
- [Ollama](https://github.com/THUDM/OLLaMa) for providing the open-source language model used in this project.
- [FAISS](https://github.com/facebookresearch/faiss) for the efficient similarity search and clustering of dense vectors.
- [HuggingFace](https://huggingface.co/) for the pre-trained text embeddings.
- [React.js](https://reactjs.org/) for the frontend user interface library.
- [Flask](https://flask.palletsprojects.com/) for the backend web framework.
