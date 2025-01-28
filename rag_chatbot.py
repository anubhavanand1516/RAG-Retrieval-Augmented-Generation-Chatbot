from flask import Flask, request, jsonify
import mysql.connector
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Initialize Flask app
app = Flask(__name__)

# Initialize the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the FAISS index from file
index = faiss.read_index('vector_index.index')

# Initialize GPT-2 for response generation
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")

# MySQL connection setup
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Inspireone1516@',  # Replace with your MySQL password
    'database': 'chatbot_db'
}

# Store chat history in MySQL
def store_chat_history(user_input, chatbot_response):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    query = "INSERT INTO chat_history (user_input, chatbot_response) VALUES (%s, %s)"
    cursor.execute(query, (user_input, chatbot_response))
    connection.commit()
    cursor.close()
    connection.close()

# Retrieve the top-k most relevant chunks
def retrieve_top_k(query, k=3):
    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)
    return I[0]

# Generate an answer using RAG approach (Retrieve relevant chunks and generate response)
def generate_answer(query, top_k_chunks):
    context = " ".join(top_k_chunks) + " " + query
    inputs = tokenizer.encode(context, return_tensors="pt", max_length=1024, truncation=True)
    outputs = gpt2_model.generate(inputs, max_length=150, num_return_sequences=1)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer

# Route to chat with the chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['user_input']

    # Retrieve top-k relevant chunks based on query
    top_k_indices = retrieve_top_k(user_input)
    top_k_chunks = [chunks[i] for i in top_k_indices]

    # Generate the chatbot's answer
    chatbot_response = generate_answer(user_input, top_k_chunks)

    # Store the conversation history in MySQL
    store_chat_history(user_input, chatbot_response)

    # Return the response and optionally top chunks for debugging
    return jsonify({'response': chatbot_response, 'top_chunks': top_k_chunks})

# Route to view the chat history
@app.route('/history', methods=['GET'])
def history():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT user_input, chatbot_response, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT 10")
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return jsonify(history)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
