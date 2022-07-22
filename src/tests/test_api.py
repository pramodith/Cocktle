import unittest
from src.parse_data import get_all_cocktails, get_all_ingredients_cocktails

class MyTestCase(unittest.TestCase):
    def test_get_all_cocktails(self):
        resp = get_all_cocktails("https://www.thecocktaildb.com/api/json/v1/1/search.php")
        self.assertEqual(True, resp)  # add assertion here

    def test_get_all_ingredients_cocktails(self):
        resp = get_all_ingredients_cocktails("https://www.thecocktaildb.com/api/json/v1/1/search.php")
        self.assertEqual(True, resp)  # add assertion here

if __name__ == '__main__':
    unittest.main()
