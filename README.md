# Nepali Font Mapper

A Python package for mapping legacy Nepali fonts to Unicode, with built-in language detection capabilities.

## Features

- **Language Detection**: 
  - Uses Levenshtein distance algorithm for word similarity matching
  - Employs cosine similarity with pre-trained sentence embeddings for accurate language detection
  - Configurable similarity threshold for fine-tuning detection accuracy

- **Font Mapping**: 
  - Maps characters from legacy Nepali fonts (like Preeti) to Unicode Nepali
  - Handles complex character combinations and special cases
  - Preserves non-Nepali text in mixed-language content
  - Supports multiple legacy font formats

## Installation
```bash
git clone https://github.com/amritregmi26/np-font-mapper.git
cd np-font-mapper
```
```bash
pip install -e .
```

This command will install the package with the name np-font-mapper.

## Quick Start

```python
from np_font_mapper import FontMapper

# Initialize the mapper
mapper = FontMapper()

# Optional: Adjust similarity threshold for language detection (default is 0.70)
mapper.similarity_threshold = 0.8

# Basic usage - maps Preeti font to Unicode
text = ";Ë|fxno" 
result = mapper.map(text)
print(result)  # Output: सङ्ग्राहलय
```

### Working with Different Fonts

```python
# Check available fonts
print(mapper.available_fonts)

# Specify a different font
result = mapper.map("your_text", font="kantipur")
```

## How It Works

1. **Language Detection**:
   - Words are analyzed using Levenshtein distance and cosine similarity
   - Pre-trained embeddings help identify English language content
   - English text is preserved in its original form

2. **Font Mapping**:
   - Characters are mapped using a comprehensive character map
   - Special character combinations are handled appropriately
   - Post-processing rules ensure correct rendering


### FontMapper Class

```python
class FontMapper:
    def __init__(self, similarity_threshold=0.70):
        """
        Initialize FontMapper with optional similarity threshold.
        
        Args:
            similarity_threshold (float): Threshold for language detection (0.0 to 1.0)
        """

    def map(self, text: str, font: str = None) -> str:
        """
        Map input text to Unicode Nepali.
        
        Args:
            text (str): Input text in legacy font
            font (str, optional): Font to use for mapping. Defaults to 'preeti'
            
        Returns:
            str: Mapped text in Unicode Nepali
        """
```

## Supported Fonts

- Preeti (Default)
- Kantipur
- Himali-TT
- PCS-Nepali
- Sagarmatha

## Common Issues and Solutions

1. **Incorrect Language Detection**:
   - Adjust `similarity_threshold` based on your text length

2. **Special Character Combinations**:
   - The mapper handles special cases like "पm" → "फ"
   - If you find any incorrect mappings, please report them

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- Additional font support
- Improved language detection
- Bug fixes and edge cases
- Documentation improvements

## License

This project is licensed under the [MIT License](https://github.com/amritregmi26/np-font-mapper/blob/main/LICENSE).

## Acknowledgments

Font mapping rules and character sets are referenced from [nep-ttf2utf](https://github.com/sapradhan/nep-ttf2utf) and [ttf-to-unicode](https://github.com/nepali-bhasa/ttf-to-unicode).

## Support

Give a Star ⭐ to support this repository!

For issues, questions, or suggestions open an issue on GitHub.