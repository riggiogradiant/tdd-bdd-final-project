# Copyright 2016, 2023 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_models.py:TestProductModel

"""
import os
import logging
import unittest
from service.models import Product, Category, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)


######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestProductModel(unittest.TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(
            name="Fedora",
            description="A red hat",
            price=12.50,
            available=True,
            category=Category.CLOTHS,
        )
        self.assertEqual(str(product), "<Product Fedora id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Fedora")
        self.assertEqual(product.description, "A red hat")
        self.assertEqual(product.available, True)
        self.assertEqual(product.price, 12.50)
        self.assertEqual(product.category, Category.CLOTHS)

    # def test_add_a_product(self):
    #     """It should Create a product and add it to the database"""
    #     products = Product.all()
    #     self.assertEqual(products, [])
    #     product = ProductFactory()
    #     product.id = None
    #     product.create()
    #     # Assert that it was assigned an id and shows up in the database
    #     self.assertIsNotNone(product.id)
    #     products = Product.all()
    #     self.assertEqual(len(products), 1)
    #     # Check that it matches the original product
    #     new_product = products[0]
    #     self.assertEqual(new_product.name, product.name)
    #     self.assertEqual(new_product.description, product.description)
    #     self.assertEqual(Decimal(new_product.price), product.price)
    #     self.assertEqual(new_product.available, product.available)
    #     self.assertEqual(new_product.category, product.category)

    #
    # ADD YOUR TEST CASES HERE
    #
    def test_read_a_product(self):
        """Read a product test"""
        product = ProductFactory()  # Crea el producto utilizando la fábrica

        product.create()  # Asegúrate de guardar el producto en la base de datos

        logging.info(f"Name: {product.name}")
        logging.info(f"Description: {product.description}")
        logging.info(f"Price: {product.price}")
        logging.info(f"Available: {product.available}")
        logging.info(f"Category: {product.category}")

        self.assertIsNotNone(product.id)  # Verifica que el ID no sea None

        # Busca el producto por ID en la base de datos
        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    def test_update_product(self):
        """Update product"""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        logging.info(f"Name: {product.name}")
        logging.info(f"Description: {product.description}")
        logging.info(f"Price: {product.price}")
        logging.info(f"Available: {product.available}")
        logging.info(f"Category: {product.category}")
        product.description = "CHANGED_DESCRIPTION"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "CHANGED_DESCRIPTION")

        all_products = Product.all()
        self.assertEqual(len(all_products), 1)
        self.assertEqual(all_products[0].id, original_id)
        self.assertEqual(all_products[0].description, "CHANGED_DESCRIPTION")

    def test_delete_product(self):
        """Delete a product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_products(self):
        """List all products"""
        products = Product.all()
        self.assertEqual(len(products), 0)

        for _ in range(5):
            product = ProductFactory()
            product.create()

        products_added = Product.all()
        logging.info(products_added)
        self.assertEqual(len(products_added), 5)

    def test_find_product_by_name(self):
        """Find product by name"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_product_by_availability(self):
        """Find product by availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_find_product_by_category(self):
        """Find product by category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_find_product_by_price(self):
        """Find product by price"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.price = str(product.price)
            product.create()
        price = products[0].price
        count = len([product for product in products if product.price == price])
        found = Product.find_by_price(price)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.price, price)

    def test_update_product_without_id(self):
        """Test that update raises an exception when the product does not have an ID"""
        product = ProductFactory()
        product.id = None  # Le damos un ID vacío para simular el error

        with self.assertRaises(Exception):
            product.update()

    # def test_deserialize_missing_field(self):
    #     """Test that deserialize raises DataValidationError when a required field is missing"""

    #     product = Product()  # Asumiendo que `Product` es la clase que contiene el método `deserialize`
    #     product.available = None
    #     with self.assertRaises(Exception) as cm:
    #         product.deserialize(data)
