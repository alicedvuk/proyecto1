import os
from random import sample
from itertools import cycle
from django.core.management import BaseCommand, call_command
from django.conf import settings

from vv.merchants.factories import MerchantFactory
from vv.merchants.models import Category, Merchant
from vv.products.factories import ProductFactory, VariantFactory
from vv.products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('loaddata', os.path.join(settings.BASE_DIR, '../fixtures/categories.json'), interactive=False)

        categories = cycle(Category.objects.all())
        merchants = []

        for _i, category in zip(range(100), categories):
            merchant = MerchantFactory(category=category)
            merchants.append(merchant)

            for _j in range(10):
                product = ProductFactory(merchant=merchant)

                VariantFactory(product=product)
                VariantFactory(product=product, price_override=product.price.gross + 10)
                VariantFactory(product=product, price_override=product.price.gross + 50)

                print('.', end='')
                self.stdout.flush()

        featured_ids = [m.id for m in sample(merchants, 12)]
        Merchant.objects.filter(id__in=featured_ids).update(featured=True)

        popular_ids = [m.id for m in sample(merchants, 12)]
        Merchant.objects.filter(id__in=popular_ids).update(popular=True)

        print()
        print('Merchants: %s' % Merchant.objects.filter().count())
        print('Products: %s' % Product.objects.filter().count())
