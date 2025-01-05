import re
from . import data_map

class FontMapper:
    def __init__(self, _similarity_threshold = 0.70) -> None:
        self._similarity_threshold = _similarity_threshold
        self.rules = self._get_rules()  
        self._detector = None
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
        if self._detector:
            self._detector.similarity_threshold = value

    def initialize_detector(self):
        """
        Initializes the language detector.
        """
        if self._detector is None:
            from .language_detection import DetectLanguage
            self._detector = DetectLanguage(self._similarity_threshold)
        return self._detector

    def _get_detector(self):
        """
        Lazily initializes and returns the language detector
        """
        return self._detector
    
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

    def map(self, text: str, map_only=False, font=None) -> str:
        """
        Maps the input text to the specified font, handling each word individually and preserving non-Nepali words.

        Args:
            text (str): The input text to map.
            map_only (bool, optional): If True, avoids language detection. Defaults to False.
            font (str, optional): The font to use for mapping. Defaults to None.

        Returns:
            str: The text with mapped fonts for Nepali words, and original text for non-Nepali words if map_only is False.

        Raises:
            ValueError: If language detection is required but the detector is uninitialized.
        """
        if not map_only and not self._detector:
            raise ValueError("Language detector is not initialized. Please call initialize_detector() first.")
    
        result = []
        if not map_only:
            detector = self._get_detector()

        for word in text.split(" "):
            if map_only or (detector and detector.detect_language(word) == 'ne-NP'):
                result.append(self._map_font(word, font))
            else:
                result.append(word)

        return " ".join(result)

