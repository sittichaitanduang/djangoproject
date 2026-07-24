from django.test import TestCase

from shop.management.commands.load_products import PRODUCTS


class ProductSeedDataTests(TestCase):
    def test_seed_products_contains_200_items(self):
        self.assertEqual(len(PRODUCTS), 200)
