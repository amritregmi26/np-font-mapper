import re
import nltk
import Levenshtein
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
        self.similarity_threshold = similarity_threshold


    def detect_language(self, query: str) -> str:
        """
        Detects the language of given query using special characters and Levenshtein ratio.
        Returns "en-US" for English or "ne-NP" for Nepali.
        """
        if not query.strip():
            return "en-US"

        pattern = (
            r'[!@#$%^&*{}[\]/]?\w*[!@#$%^&*{}[\]/]\w*|'  
            r'\w*[!@#$%^&*{}[\]/]\w*|'                   
            r'\([^)\s]*\)|'                               
            r'\([^)\s]*|'                                 
            r'[^(\s]*\)'                                  
        )

        matches = re.findall(pattern, query)
        
        if not matches:
            max_similarity = max(
                Levenshtein.ratio(query.strip(), word) 
                for word in self.words
            )
            return "en-US" if max_similarity >= self.similarity_threshold else "ne-NP"

        processed_word = matches[0]
        if re.search(r'[!@#$%^&*{}[\]/]', processed_word):
            return "ne-NP"

        processed_word = (
            processed_word[1:-1] if processed_word.startswith("(") and processed_word.endswith(")") else
            processed_word[1:] if processed_word.startswith("(") else
            processed_word[:-1] if processed_word.endswith(")") else
            processed_word
        ).lower().strip()

        max_similarity = max(
            Levenshtein.ratio(processed_word, word) 
            for word in self.words
        )
        
        return "en-US" if max_similarity >= self.similarity_threshold else "ne-NP"