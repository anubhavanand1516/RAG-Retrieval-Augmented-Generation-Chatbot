
# RAG Chatbot System

This repository contains a RAG (Retrieve & Generate) chatbot system that integrates MySQL, FAISS for vector storage, and SentenceTransformers for text embeddings. It allows you to interact with the chatbot via REST API endpoints, store and retrieve conversation history in MySQL.

## 1. Install and Run the System Locally

### Install Dependencies

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/rag-chatbot.git
   cd rag-chatbot
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   conda create -n rag python=3.10
   conda activate rag
   ```

3. Install the required Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Run the Application

Start the Flask app locally:

```bash
python rag_chatbot.py
```

The application will be running at `http://127.0.0.1:5000`.

## 2. Set Up MySQL and Create the Required Tables

### Install MySQL

If you don’t already have MySQL installed, follow the steps for your operating system:

- **macOS**: Install using Homebrew:
  ```bash
  brew install mysql
  ```
  
- **Ubuntu**:
  ```bash
  sudo apt install mysql-server
  ```

### Create the Database and User

1. Log into MySQL:

   ```bash
   mysql -u root -p
   ```

2. Create the database and user:

   ```sql
   CREATE DATABASE rag_chatbot;
   CREATE USER 'rag_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON rag_chatbot.* TO 'rag_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

3. Create the required `history` table:

   ```sql
   USE rag_chatbot;

   CREATE TABLE history (
       id INT AUTO_INCREMENT PRIMARY KEY,
       user_message TEXT,
       bot_response TEXT,
       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

## 3. Environment Variables

Create a `.env` file in the project directory with the following contents:

```env
DB_HOST=localhost
DB_USER=rag_user
DB_PASSWORD=password
DB_NAME=rag_chatbot
```

This file will provide the database credentials needed for the system to connect to MySQL.

## 4. Python Files

### `data_preprocessing.py`

This script is responsible for processing and preparing the input data (e.g., cleaning text or creating embeddings). It uses libraries like `sentence_transformers` to generate embeddings for text.


### `embed_store.py`

This script handles storing the generated embeddings into a FAISS index, which is used to perform fast similarity searches.


### `rag_chatbot.py`

This file is the main Flask application. It defines the routes and handles the interactions between the user and the chatbot. It retrieves the user message, processes it, and generates a response.


### `requirements.txt`

This file contains the list of required Python dependencies. Ensure all necessary libraries are added here.

```
Flask==2.1.1
mysql-connector-python==8.0.27
faiss-cpu==1.7.1
sentence-transformers==2.2.0
huggingface-hub==0.9.0
sklearn==0.0
python-dotenv==0.19.2
```

## 5. Test the Endpoints

### Test the `/chat` Endpoint

- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "message": "Hello, chatbot!"
  }
  ```
- **Example Response**:
  ```json
  {
    "response": "I'm here to help! You asked: Hello, chatbot!"
  }
  ```

This endpoint generates a response to the user message and stores both the user input and the bot response in the MySQL database.

### Test the `/history` Endpoint

- **Method**: `GET`
- **Example Response**:
  ```json
  [
    {
      "id": 1,
      "user_message": "Hello, chatbot!",
      "bot_response": "I'm here to help! You asked: Hello, chatbot!",
      "timestamp": "2025-01-29 12:00:00"
    }
  ]
  ```

This endpoint retrieves all stored conversations from the MySQL database.
