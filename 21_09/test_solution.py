from solution import count_vowels
import unittest

class TestCountVowels(unittest.TestCase):
    
    def test_no_vowels(self):
        self.assertEqual(count_vowels('rhytm'), 0)
        
    def test_only_vowels(self):
        self.assertEqual(count_vowels('aeiouAEIOU'), 10)
        
    def test_normal_text_vowels(self):
        self.assertEqual(count_vowels('gotoschoolyes'), 5)
    
    def test_random_registry_vowels(self):
        self.assertEqual(count_vowels('BasETeXtIsGOoD'), 6)
        
    def test_zero_letters_vowels(self):
        self.assertEqual(count_vowels(''),0)

if __name__=="__main__":
    unittest.main()