import re
from .language_detection import DetectLanguage
from . import data_map

class FontMapper:
    def __init__(self, _similarity_threshold = 0.70) -> None:
        self._similarity_threshold = _similarity_threshold
        self._detector = DetectLanguage(similarity_threshold=self.similarity_threshold)
        self.rules = self._get_rules()  
        self.available_fonts = self._get_available_fonts()  

    @property
    def similarity_threshold(self) -> float:
        """
        Returns the similarity threshold used for language detection.
        """
        return self._similarity_threshold
    
    @similarity_threshold.setter
    def similarity_threshold(self, value: float):
        """
        Sets the similarity threshold used for language detection.

        Args:
            value (float): The new similarity threshold value.
        """
        self._similarity_threshold = value
        self._detector.similarity_threshold = value

    def _is_unicode_nepali(self, text: str) -> bool:
        """
        Checks if a given string contains Unicode Nepali characters.

        Args:
            text (str): The string to check for Nepali Unicode characters.

        Returns:
            bool: True if the text contains Nepali Unicode characters, False otherwise.
        """
        return any('\u0900' <= char <= '\u097F' for char in text)
    
    def _get_available_fonts(self):
        """
        Returns a list of available fonts for mapping.
        """
        return list(self.rules[0].keys())[2:] 
    
    def _get_rules(self):
        """
        Returns the list of font mapping rules.
        """
        return data_map.all_rules

    def _map_font(self, text, font=None):
        """
        Maps the given text to the specified font, using the character map and post-rules.

        Args:
            text (str): The text to map to the font.
            font (str, optional): The font to use for the mapping. Defaults to 'preeti'.

        Returns:
            str: The text mapped to the specified font.
        
        Raises:
            ValueError: If the font is not available in the font rules.
        """
        if font is None:
            font = 'preeti'

        font = font.lower()
        my_font = self.rules[0].get(font, '')

        if not my_font:
            raise ValueError('Font not included in module')

        char_map = my_font['char-map']
        
        mapped_text = ''.join([char_map.get(char, char) for char in text])
        
        for rule in self.rules[0]['post-rules']:
            mapped_text = re.sub(rule[0], rule[1], mapped_text)
        
        return mapped_text
    
    def _normalize_characters(self, input_string):
        """
        Rearranges the input string such that:
        - 'l' or 'L' moves one step after the next letter.
        - '{' moves one position before the current position.
        This process helps to fix the problem related to इकार and र्
        """
        def _normalize_word(word):
            chars = list(word)
            i = 0
            while i < len(chars):
                if chars[i].lower() == 'l' and i < len(chars) - 1:
                    chars[i], chars[i+1] = chars[i+1], chars[i]
                    i += 2
                elif chars[i] == '{' and i > 0:
                    chars[i], chars[i-1] = chars[i-1], chars[i]
                    i += 1
                else:
                    i += 1
            return ''.join(chars)
        return ' '.join(_normalize_word(word) for word in input_string.split())

    def map(self, text: str, font=None) -> str:
        """
        Maps the input text to the specified font, handling each word individually and preserving non-Nepali words.

        Args:
            text (str): The input text to map.
            font (str, optional): The font to use for mapping. Defaults to None.

        Returns:
            str: The text with mapped fonts for Nepali words, and original text for non-Nepali words.
        """
        result = []
        normalized_text = self._normalize_characters(text)
        for word in normalized_text.split(" "):
            if self._detector.detect_language(word) == 'ne-NP':
                mapped_word = []
                for char in word: 
                    if not self._is_unicode_nepali(char):
                        mapped_word.append(self._map_font(char, font))
                    else:
                        mapped_word.append(char)
                result.append(''.join(mapped_word))
            else:
                result.append(word)

        for idx, word in enumerate(result):
            has_english = re.search(r'[a-zA-Z]', word)
            if has_english:
                for rule in self.rules[0]['post-rules']:
                    mapped_word = re.sub(rule[0], rule[1], word)
                    has_english = re.search(r'[a-zA-Z]', mapped_word)
                    if not has_english:
                        result[idx] = mapped_word
                        break
        
        return " ".join(result)
