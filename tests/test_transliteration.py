"""Tests for Gurmukhi transliteration"""
import pytest
from backend.services.transliteration import (
    GurmukhiTransliterator,
    get_transliterator,
    transliterate_gurmukhi_to_roman
)


class TestGurmukhiTransliterator:
    """Test Gurmukhi to Romanised Punjabi transliteration"""
    
    def test_basic_consonants(self):
        """Test basic consonant transliteration"""
        transliterator = GurmukhiTransliterator()
        
        # Test individual consonants (with inherent 'a')
        assert 'ka' in transliterator.transliterate('ਕ')
        assert 'sa' in transliterator.transliterate('ਸ')
        assert 'pa' in transliterator.transliterate('ਪ')
    
    def test_vowels(self):
        """Test independent vowel transliteration"""
        transliterator = GurmukhiTransliterator()
        
        assert 'a' in transliterator.transliterate('ਅ')
        assert 'aa' in transliterator.transliterate('ਆ')
        assert 'i' in transliterator.transliterate('ਇ')
    
    def test_word_transliteration(self, sample_gurmukhi_text):
        """Test full word transliteration"""
        result = transliterate_gurmukhi_to_roman(sample_gurmukhi_text)
        
        # Result should be non-empty and contain latin characters
        assert result
        assert len(result) > 0
        # Should contain some expected sounds
        assert any(char.isalpha() for char in result)
    
    def test_empty_string(self):
        """Test empty string handling"""
        result = transliterate_gurmukhi_to_roman("")
        assert result == ""
    
    def test_singleton_pattern(self):
        """Test that get_transliterator returns same instance"""
        trans1 = get_transliterator()
        trans2 = get_transliterator()
        assert trans1 is trans2
    
    def test_special_characters_preserved(self):
        """Test that punctuation is preserved"""
        transliterator = GurmukhiTransliterator()
        
        result = transliterator.transliterate("ਕ?")
        assert '?' in result
        
        result = transliterator.transliterate("ਕ।")
        assert '.' in result

