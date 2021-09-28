import errno
import json
import logging
import os
from typing import List

import requests
from django.conf import settings
from django.db import IntegrityError, DataError, transaction
from pytils.translit import slugify

from shop.models import Category, Vendor, Product, Attribute, AttributesCategory

logger = logging.getLogger(__name__)


class BaseJSONParser:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def _encoded_json(self):
        file = open(self.file_path, 'r+')
        data = json.loads(file.read())
        return data


class CategoryParser(BaseJSONParser):

    def __call__(self):
        data = self._encoded_json()
        print("Data was uploaded")
        for category_name, category_data in data.items():
            subcategories_data = category_data.pop('subcategories')
            category = self._parse_parent_category(category_data)
            print(f"Parent category {category.name} was created")
            products_to_create = []
            for key, subcategory in subcategories_data.items():
                if subcategory.get('products'):
                    products_to_create.append(
                        {'data': subcategory.pop('products'), 'category_slug': subcategory['slug']})
                subcategory_object = self._parse_subcategories(subcategory, category)
            if products_to_create:
                self._parse_products(products_to_create)

    @staticmethod
    def _download_image(file_name: str, file_url: str = None):
        if not file_url:
            return None
        extension = file_url.split('.')[-1]
        file_name = '/categories/images/' + file_name + '.' + extension
        file_path = settings.MEDIA_ROOT + file_name
        if not os.path.exists(os.path.dirname(file_path)):
            try:
                os.makedirs(os.path.dirname(file_path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(file_path, 'wb') as file:
            response = requests.get(file_url)
            if not response.ok:
                return
            for block in response.iter_content(1024):
                if not block:
                    break
                file.write(block)
        return file_name

    def _parse_parent_category(self, data: dict):
        data.pop('link')
        if 'id' in data.keys():
            data.pop('id')
        data['image'] = self._download_image(data['slug'], data['image'])
        slug = data.pop('slug')
        return Category.objects.get_or_create(defaults={**data}, slug=slug)[0]

    def _parse_subcategories(self, data: dict, parent_category: Category):
        subcategories = {}
        products_to_create = []
        data.pop('id')
        if 'subcategories' in data.keys():
            subcategories = data.pop('subcategories')
        if 'products' in data.keys():
            products_to_create.append({'category_slug': data['slug'], 'data': data.pop('products')})
        if 'link' in data.keys():
            data.pop('link')
        data['image'] = self._download_image(data['slug'], data['image'])
        data['parent'] = parent_category
        slug = data['slug']
        category = Category.objects.get_or_create(defaults={**data}, slug=slug)[0]
        print(f"Subcategory {category.name} was created with parent {parent_category.name}")
        if subcategories:
            for key, subcategory in subcategories.items():
                self._parse_subcategories(subcategory, category)
        if products_to_create:
            self._parse_products(products_to_create)
        return category

    def _parse_products(self, data: List[dict]):
        category_slugs = [item.get('category_slug') for item in data]
        categories = Category.objects.filter(slug__in=category_slugs)
        categories_for_products = {category.slug: category for category in categories}
        for item in data[0]['data']:
            if 'features' in item.keys():
                item.pop('features')

            params = item.pop('params')
            attributes = []
            for param in params:
                if param.get('id').startswith('string'):
                    param['string_value'] = param.pop('value')
                    param['float_value'] = 0.0

                else:
                    param['float_value'] = param.pop('value')
                    if param['float_value'] == 'None':
                        param['float_value'] = 0.0

                param.pop('id')
                param['slug'] = slugify(param['name'])
                category = AttributesCategory.objects.get_or_create(defaults={'name': param.pop('name')},
                                                                    **{'slug': param.pop('slug')})[0]
                param['category'] = category
                attribute = Attribute.objects.get_or_create(**param)[0]
                attributes.append(attribute)
            vendor_data = item.pop('vendor')
            vendor = None
            if vendor_data:
                vendor_data.pop('id')
                vendor_data['image'] = vendor_data.pop('thumbnail')
                try:
                    vendor = Vendor.objects.get_or_create(defaults={**vendor_data}, **{'slug': vendor_data['slug']})[0]
                except IntegrityError:
                    pass
            item.pop('short_name')
            item.pop('thumbnail')
            item.pop('seo')
            item['slug'] = slugify(item['name'])
            if item['image']:
                item['preview'] = self._download_image(item['slug'], item.pop('image'))
            category = categories_for_products.get(data[0]['category_slug'])
            try:
                slug = item['slug']
                item['cash_price'] = item.pop('price_cash')
                if not item['cash_price']:
                    item['cash_price'] = 0
                item['price'] = item.pop('price_cashless')
                if not item['price']:
                    item['price'] = 0
                product = Product.objects.get_or_create(defaults={
                    'category': category,
                    'vendor': vendor,
                    **item
                }, slug=slug)[0]
                product.attributes.set(attributes)
                product.save()
                print(f"Product {product.name} was created with category {category.name}")
            except DataError:
                pass
