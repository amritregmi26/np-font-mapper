import nltk
import torch.nn.functional as F
import Levenshtein
from sentence_transformers import SentenceTransformer
from typing import List
import warnings

warnings.filterwarnings("ignore")

class DetectLanguage:
    def __init__(self, similarity_threshold) -> None:
        try:
            english_words = nltk.corpus.words.words()
        except LookupError:
            nltk.download('words')
            english_words = nltk.corpus.words.words()
        
        self.words = set(word.lower() for word in english_words)
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.similarity_threshold = similarity_threshold

    def _similar_words(self, query: str, k=10, length_margin=5) -> List[str]:
        """
        Finds words in the English corpus that are similar to the given query based on Levenshtein distance.

        Args:
            query (str): The query word to find similar words for.
            k (int, optional): The number of similar words to return. Defaults to 10.
            length_margin (int, optional): The allowable difference in length between the query word and the candidate words. Defaults to 2.

        Returns:
            List[str]: A list of words from the English corpus that are similar to the query.
        """
        query_len = len(query)
        
        # Only consider words with a length within the margin from the query word's length
        candidate_words = [word for word in self.words if abs(len(word) - query_len) <= length_margin]

        # Compute Levenshtein distance for each candidate word and sort them by similarity
        distances = {word: Levenshtein.distance(query.lower(), word) for word in candidate_words}
        similar_words = sorted(distances.items(), key=lambda x: x[1])

        # Return the top k similar words
        similar_words = [word for word, _ in similar_words[:k]]
        return similar_words

    def _get_cosine_similarity(self, query: str) -> List[float]:
        """
        Computes cosine similarity between the query and its most similar words based on Levenshtein distance.

        Args:
            query (str): The query word to compare with similar words.

        Returns:
            List[float]: A list of cosine similarity scores between the query and the similar words.
        """
        similar_levenshtein_words = self._similar_words(query)
        embeddings = self.embedding_model.encode(similar_levenshtein_words, convert_to_tensor=True)
        input_vector = self.embedding_model.encode(query.lower(), convert_to_tensor=True).unsqueeze(0)
        cosine_similarities = F.cosine_similarity(embeddings, input_vector, dim=1)
        return cosine_similarities.tolist()

    def detect_language(self, query: str) -> str:
        """
        Detects the language of the given query by comparing its cosine similarity to the most similar English words.

        Args:
            query (str): The input query to detect the language for.

        Returns:
            str: "en-US" if the query is determined to be in English, or "ne-NP" if it is determined to be in Nepali.
        """
        cosine_similarities = self._get_cosine_similarity(query)
        max_similarity = max(cosine_similarities)
        if max_similarity >= self.similarity_threshold:
            return "en-US"
        else:
            return "ne-NP"
