import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load preprocessed text chunks (you can load them from a file or define them here)
with open('chunks.txt', 'r') as f:
    chunks = f.readlines()

# Convert the chunks into embeddings
embeddings = model.encode(chunks)

# Initialize FAISS index
dimension = embeddings.shape[1]  # Embedding dimension
index = faiss.IndexFlatL2(dimension)  # L2 distance index

# Add embeddings to FAISS index
index.add(np.array(embeddings))

# Save FAISS index to file (optional for later retrieval)
faiss.write_index(index, 'vector_index.index')

print("Embeddings stored in FAISS index.")
