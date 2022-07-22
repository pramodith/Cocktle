import unittest
from src.parse_data import get_all_cocktails, get_all_ingredients_cocktails
from src.utils import levenshtein_distance

class MyTestCase(unittest.TestCase):
    def test_get_all_cocktails(self):
        resp = get_all_cocktails("https://www.thecocktaildb.com/api/json/v1/1/search.php")
        self.assertEqual(True, resp)  # add assertion here

    def test_get_all_ingredients_cocktails(self):
        resp = get_all_ingredients_cocktails("https://www.thecocktaildb.com/api/json/v1/1/search.php")
        self.assertEqual(True, resp)  # add assertion here

    def test_levenshtein_distance(self):
        resp = levenshtein_distance("afdg", "sagg")
        '''
        Delete s,g
        Insert f,d
        Total 4
        '''
        self.assertEqual(4, resp)
        resp = levenshtein_distance("Vermouth Cassis", "Vermouth Casis")
        '''
        Insert s,d
        '''
        self.assertEqual(1, resp)


if __name__ == '__main__':
    unittest.main()
