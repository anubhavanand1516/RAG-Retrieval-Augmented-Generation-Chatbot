import re
from sentence_transformers import SentenceTransformer

# Preprocess text: clean extra whitespaces and normalize
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Split large documents into smaller chunks
def chunk_text(corpus, chunk_size=200):
    chunks = []
    for doc in corpus:
        words = doc.split()
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(preprocess_text(chunk))
    return chunks

# Load a small sample corpus (You can replace this with your own corpus)
corpus = [
    "Artificial Intelligence (AI) is the simulation of human intelligence processes by machines, especially computer systems.",
    "These processes include learning, reasoning, problem-solving, perception, and language understanding.",
    "AI is applied in many areas such as machine learning, robotics, natural language processing, and computer vision.",
    "Deep learning, a subset of machine learning, has significantly advanced AI research and applications.",
    "Artificial intelligence systems can be divided into narrow AI (task-specific) and general AI (human-level intelligence)."
]

# Chunk the corpus into smaller chunks
chunks = chunk_text(corpus)

# Save chunks to a file (optional)
with open('chunks.txt', 'w') as f:
    for chunk in chunks:
        f.write(chunk + '\n')

print(f"Total Chunks: {len(chunks)}")
