import re
import json
from language_detection import DetectLanguage

class FontMapper:
    def __init__(self) -> None:
        self.detector = DetectLanguage()

    def _is_unicode_nepali(self, text: str) -> bool:
        return len(list(text.encode('utf-8'))) > 1
    
    def get_available_fonts(self):
        return list(self.get_rules()[0].keys())[2:] 
    
    def get_rules(self):
        with open('../data/data-map.json', 'r') as file:
            return json.load(file)   

    def _map_font(self, text, font=None):
        # Default to Preeti if no font is provided
        if font is None:
            font = 'preeti'

        rules = self.get_rules()
        font = font.lower()
        my_font = rules[0].get(font, '')

        if not my_font:
            raise ValueError('Font not included in module')
        
        output = ''
        
        # Replace characters based on char-map
        for letter in text:
            output += my_font['char-map'].get(letter, letter)
        
        # Apply post-rules using regular expressions
        for rule in rules[0]['post-rules']:
            output = re.sub(rule[0], rule[1], output)
        
        return output
    
    def map(self, text, font=None):
        result = []
        for item in text.split(" "):
            if self.detector.detect_language(item) == 'ne-NP':
                word = ""
                for char in item: 
                    if not self._is_unicode_nepali(char):
                        unicode_text = self._map_font(char, font)
                        word += unicode_text
                    else:
                        word += char
                result.append(word)
            else:
                result.append(item)
        return " ".join(result)