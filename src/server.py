from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route('/chat', methods=['POST'])
def chat():
    query = request.json['query']
    use_vector_embeddings = request.json['useVectorEmbeddings']

    # Run your Python script with the query as input
    print(query)
    # result = subprocess.run(['python3', 'fakeRAG.py', query], capture_output=True, text=True)
    result = subprocess.run(['python3', 'RAGandLLM.py', query,str(use_vector_embeddings)], capture_output=True, text=True)
    # result = subprocess.run(['python3', 'RAG.py', query], capture_output=True, text=True)
    print(result)
    response = result.stdout
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)