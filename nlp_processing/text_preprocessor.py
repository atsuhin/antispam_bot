import re
import emoji

class TextPreprocessor:
    def __init__(self):
        """Initialize the text preprocessor"""
        pass
        
    def clean_text(self, text):
        """
        Clean and preprocess the input text
        
        Args:
            text (str): Input text to clean
            
        Returns:
            str: Cleaned text
        """
        text = text.lower()
        text = emoji.replace_emoji(text, '')
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^а-яё\s]', '', text)
        text = text.replace('ё', 'е')
        
        return text.strip() 