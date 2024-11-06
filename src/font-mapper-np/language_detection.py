import nltk
import torch
import torch.nn.functional as F
import Levenshtein
from sentence_transformers import SentenceTransformer
from typing import List


class DetectLanguage:
    def __init__(self) -> None:
        try:
            english_words = nltk.corpus.words.words()
        except LookupError as e:
            nltk.download('words')
            english_words = nltk.corpus.words.words()
        self.words = set(word.lower() for word in english_words)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.similarity_threshold = 0.70

    def _similar_words(self, query: str , k = 10) -> List[str]:
        distances = {}
        for word in self.words:
            distances[word] = Levenshtein.distance(query.lower(), word)
        similar_words = sorted(distances.items(), key=lambda x: x[1])
        similar_words = [word for word, _ in similar_words[:k]]
        return similar_words
    
    def _get_cosine_similarity(self, query: str) -> List[float]:
        similar_levenshtein_words = self._similar_words(query)
        embeddings = self.embedding_model.encode(similar_levenshtein_words)
        input_vector = torch.tensor(self.embedding_model.encode(query.lower()))
        cosine_similarities = []
        for embedding in embeddings:
            embd = torch.tensor(embedding)
            cosine_similarities.append(F.cosine_similarity(embd, input_vector, dim=0).item())
        return cosine_similarities
    
    def detect_language(self, query: str) -> str:
        cosine_similarities = self._get_cosine_similarity(query)
        max_similarity = max(cosine_similarities)
        if max_similarity >= self.similarity_threshold:
            return "en-US"
        else:
            return "ne-NP"
        