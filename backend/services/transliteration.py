"""Gurmukhi to Romanised Punjabi transliteration"""
from typing import Dict


class GurmukhiTransliterator:
    """Transliterate Gurmukhi script to Romanised Punjabi"""
    
    # Gurmukhi consonants to Roman mapping
    CONSONANTS: Dict[str, str] = {
        'ਸ': 's', 'ਹ': 'h', 'ਕ': 'k', 'ਖ': 'kh', 'ਗ': 'g', 'ਘ': 'gh', 'ਙ': 'ng',
        'ਚ': 'ch', 'ਛ': 'chh', 'ਜ': 'j', 'ਝ': 'jh', 'ਞ': 'ny',
        'ਟ': 't', 'ਠ': 'th', 'ਡ': 'd', 'ਢ': 'dh', 'ਣ': 'n',
        'ਤ': 't', 'ਥ': 'th', 'ਦ': 'd', 'ਧ': 'dh', 'ਨ': 'n',
        'ਪ': 'p', 'ਫ': 'ph', 'ਬ': 'b', 'ਭ': 'bh', 'ਮ': 'm',
        'ਯ': 'y', 'ਰ': 'r', 'ਲ': 'l', 'ਵ': 'v', 'ੜ': 'r',
    }
    
    # Gurmukhi independent vowels to Roman mapping
    VOWELS: Dict[str, str] = {
        'ਅ': 'a', 'ਆ': 'aa', 'ਇ': 'i', 'ਈ': 'ee', 'ਉ': 'u', 'ਊ': 'oo',
        'ਏ': 'e', 'ਐ': 'ai', 'ਓ': 'o', 'ਔ': 'au',
    }
    
    # Gurmukhi vowel diacritics (matras) to Roman mapping
    MATRAS: Dict[str, str] = {
        'ਾ': 'aa', 'ਿ': 'i', 'ੀ': 'ee', 'ੁ': 'u', 'ੂ': 'oo',
        'ੇ': 'e', 'ੈ': 'ai', 'ੋ': 'o', 'ੌ': 'au',
        'ੰ': 'n', 'ਂ': 'n', 'ੱ': '', '਼': '',  # Nasalization and other marks
    }
    
    # Special characters
    SPECIALS: Dict[str, str] = {
        '।': '.', '॥': '||', 'ੴ': 'ik onkar',
        ' ': ' ', '?': '?', '!': '!', ',': ',',
        '.': '.', '-': '-', '(': '(', ')': ')',
    }
    
    def __init__(self):
        """Initialize transliterator"""
        self.mapping = {
            **self.CONSONANTS,
            **self.VOWELS,
            **self.MATRAS,
            **self.SPECIALS
        }
    
    def transliterate(self, gurmukhi_text: str) -> str:
        """
        Transliterate Gurmukhi text to Romanised Punjabi.
        
        This is a simplified transliteration scheme. For production use,
        consider using a dedicated library or LLM-based approach for better accuracy.
        
        Args:
            gurmukhi_text: Text in Gurmukhi script
        
        Returns:
            Romanised Punjabi text
        """
        if not gurmukhi_text:
            return ""
        
        result = []
        i = 0
        text_len = len(gurmukhi_text)
        
        while i < text_len:
            char = gurmukhi_text[i]
            
            # Check for direct mapping
            if char in self.mapping:
                roman = self.mapping[char]
                
                # If it's a consonant, check for following matra
                if char in self.CONSONANTS:
                    # Default inherent 'a' vowel
                    result.append(roman + 'a')
                    
                    # Check next character for matra
                    if i + 1 < text_len and gurmukhi_text[i + 1] in self.MATRAS:
                        # Remove inherent 'a' and add matra
                        result[-1] = roman + self.MATRAS[gurmukhi_text[i + 1]]
                        i += 1  # Skip matra
                    elif i + 1 < text_len and gurmukhi_text[i + 1] == '੍':
                        # Halant - remove inherent vowel
                        result[-1] = roman
                        i += 1  # Skip halant
                else:
                    result.append(roman)
            else:
                # Unknown character, keep as-is
                result.append(char)
            
            i += 1
        
        return ''.join(result)
    
    def transliterate_simple(self, gurmukhi_text: str) -> str:
        """
        Simplified transliteration for common words.
        This is a fallback that can be improved with LLM assistance.
        
        Args:
            gurmukhi_text: Text in Gurmukhi script
        
        Returns:
            Romanised Punjabi text
        """
        # For MVP, use basic character replacement
        # In production, this should be enhanced with proper linguistic rules
        return self.transliterate(gurmukhi_text)


# Global transliterator instance
_transliterator: GurmukhiTransliterator | None = None


def get_transliterator() -> GurmukhiTransliterator:
    """Get global transliterator instance (singleton pattern)"""
    global _transliterator
    if _transliterator is None:
        _transliterator = GurmukhiTransliterator()
    return _transliterator


def transliterate_gurmukhi_to_roman(gurmukhi_text: str) -> str:
    """
    Convenience function to transliterate Gurmukhi to Romanised Punjabi.
    
    Args:
        gurmukhi_text: Text in Gurmukhi script
    
    Returns:
        Romanised Punjabi text
    """
    return get_transliterator().transliterate(gurmukhi_text)

