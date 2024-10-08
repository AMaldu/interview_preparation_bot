import pandas as pd
from minsearch import Index
import spacy
import os

DATA_PATH = os.getenv("DATA_PATH", "../data/data.csv")

def load_data(data_path=DATA_PATH):
    """
    Load data from a CSV file and convert it into a dictionary.

    Args:
        data_path (str): Path to the CSV file.

    Returns:
        list: List of dictionaries containing the data.
    """
    try:
        df = pd.read_csv(data_path)
        documents = df.to_dict(orient='records')
        return documents
    except FileNotFoundError:
        print(f"The file at {data_path} was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return []


def chunk_data(documents):
    """
    Split documents into chunks using sentences.

    Args:
        documents (list): List of documents.

    Returns:
        list: List of dictionaries containing the chunked data.
    """
    nlp = spacy.load("es_core_news_sm")

    def split_into_sentence_chunks(text, base_id):
        doc = nlp(text)  
        sentences = [sent.text for sent in doc.sents] 

        chunked_texts = []
        current_chunk = []

        for sentence in sentences:
            current_chunk.append(sentence)

            if len(current_chunk) >= 3:  
                chunked_texts.append(' '.join(current_chunk))
                current_chunk = []  

        if current_chunk:
            chunked_texts.append(' '.join(current_chunk))

        chunk_ids = [f"{base_id}_{i + 1}" for i in range(len(chunked_texts))]

        return [{'chunk_id': chunk_id, 'chunk_text': chunk_text, 'text_id': base_id} 
                for chunk_id, chunk_text in zip(chunk_ids, chunked_texts)]

    chunked_docs = []
    for doc in documents:
        if 'text' in doc and 'text_id' in doc:  
            chunks = split_into_sentence_chunks(doc['text'], doc['text_id'])
            chunked_docs.extend(chunks)  
    return chunked_docs


def index_data(docs):
    """
    Index the provided documents.

    Args:
        docs (list): List of chunked documents.

    Returns:
        Index: The created index.
    """
    index = Index(
        text_fields=["chunk_text"],
        keyword_fields=["text_id", "chunk_id"]
    )

    return index.fit(docs)


def ingest_data():
    """
    Load, chunk, and index the data.

    Returns:
        Index: The created index with the data.
    """
    loaded_data = load_data()
    if not loaded_data:
        return None  

    chunked_data = chunk_data(loaded_data)
    indexed_data = index_data(chunked_data)
    return indexed_data
