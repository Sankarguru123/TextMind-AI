from fastapi import APIRouter
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


router = APIRouter()
nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")  # Better than TF-IDF


def preprocess_text(text):
    """Preprocess text: Remove extra spaces & lowercase"""
    return text.lower().strip()


@router.post("/answer/")
def answer_question(question: str, text: str):
    text_sentences = text.split(". ")
    processed_sentences = [preprocess_text(sent) for sent in text_sentences]

    # Encode sentences & question using BERT
    sentence_embeddings = model.encode(processed_sentences)
    question_embedding = model.encode([preprocess_text(question)])

    # Compute similarity & find best match
    similarities = cosine_similarity(question_embedding, sentence_embeddings).flatten()
    best_match_idx = similarities.argmax()

    return {"question": question, "answer": text_sentences[best_match_idx]}
