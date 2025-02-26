import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re


# Loading a pre-trained embedding model
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# Loading Hugging Face API_KEY from .env file
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('API_KEY')

# Function to scrape text from multiple URLs
def scrape_text_from_urls(urls):
    #Scrapping text from multiple webpages and removes unnecessary elements.
    all_texts = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                # Removeing unwanted elements
                for script in soup(["script", "style", "noscript", "header", "footer", "aside", "nav"]):
                    script.extract()

                # Extracting paragraphs and headings
                content = []
                for tag in soup.find_all(["p", "h1", "h2", "h3"]):
                    text = tag.get_text(strip=True)
                    if text:
                        content.append(text)

                # Storing extracted text
                all_texts.append(" ".join(content))
            else:
                all_texts.append(f"Error fetching {url} (status code {response.status_code})")
        except Exception as e:
            all_texts.append(f"Error fetching {url}: {str(e)}")
    
    return all_texts

# Chunking function of the large text
def chunk_text(text, chunk_size=700, overlap=200):
    #Spliting text into clean, sentence-boundary chunks.
    chunks = []
    sentences = re.split(r'(?<=\.)\s+', text)

    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) <= chunk_size:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence
    if chunk:
        chunks.append(chunk.strip())

    return chunks

# Creating FAISS index for multiple texts
def create_faiss_index(texts):
    """Creates a FAISS index for multiple texts from different URLs."""
    all_chunks = []
    all_embeddings = []
    
    for text in texts:
        chunks = chunk_text(text, chunk_size=700, overlap=400)
        embeddings = embedding_model.encode(chunks, normalize_embeddings=True)
        all_chunks.extend(chunks)
        all_embeddings.append(embeddings)
    
    d = embedding_model.get_sentence_embedding_dimension()
    index = faiss.IndexFlatIP(d)
    
    # Flattening and add embeddings of the chunks
    all_embeddings = np.vstack(all_embeddings)
    index.add(all_embeddings)
    
    return index, all_chunks

# Retrieving relevant chunks
def retrieve_relevant_chunks(query, index, chunks, num_results=5):
    # Retrieving relevant text chunks from FAISS index.
    query_embedding = embedding_model.encode([query], normalize_embeddings=True)
    D, I = index.search(query_embedding, num_results)
    return [chunks[i] for i in I[0] if 0 <= i < len(chunks)]

# Generating answer from Mistral LLM through huggingface API call
def get_answer_from_mistral(context, query):
    """Queries Mistral 7B to generate an answer using only retrieved context."""
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    prompt = f""" 
    Generate the Answer of the question strictly based on the provided context. If question is not related to the context then return an empty response. 
    question: {query}
    context: {context}
    """

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500, 
            "temperature": 0.01, # temperature is too low for generating deterministic answer
            "top_p": 0.99      # Considering tokens from top wide probability range.
            }
    }

    # requesting the LLM through hugging face
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_json = response.json()
        if isinstance(response_json, list) and len(response_json) > 0:
            return response_json[0].get("generated_text", "").strip()
    
    return "Error: No answer generated."
