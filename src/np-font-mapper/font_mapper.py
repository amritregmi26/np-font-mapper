import re
from language_detection import DetectLanguage
import data_map

class FontMapper:
    def __init__(self) -> None:
        self.detector = DetectLanguage()
        self.similarity_threshold = self.detector.similarity_threshold
        self.rules = self.get_rules()  
        self.available_fonts = self.get_available_fonts()  

    def _is_unicode_nepali(self, text: str) -> bool:
        """
        Checks if a given string contains Unicode Nepali characters.

        Args:
            text (str): The string to check for Nepali Unicode characters.

        Returns:
            bool: True if the text contains Nepali Unicode characters, False otherwise.
        """
        return any('\u0900' <= char <= '\u097F' for char in text)
    
    def get_available_fonts(self):
        """
        Returns a list of available fonts for mapping.
        """
        return list(self.rules[0].keys())[2:] 
    
    def get_rules(self):
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
        for word in text.split(" "):
            if self.detector.detect_language(word) == 'ne-NP':
                mapped_word = []
                for char in word: 
                    if not self._is_unicode_nepali(char):
                        mapped_word.append(self._map_font(char, font))
                    else:
                        mapped_word.append(char)
                result.append(''.join(mapped_word))
            else:
                result.append(word)
        
        return " ".join(result)
