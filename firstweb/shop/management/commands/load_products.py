from pathlib import Path

import openpyxl
from django.core.management.base import BaseCommand

from shop.models import Brand, Category, Product


def load_products_from_excel():
    candidate_paths = [
        Path(__file__).resolve().parents[3] / 'computer_products_100.xlsx',
        Path(__file__).resolve().parents[4] / 'computer_products_100.xlsx',
        Path(__file__).resolve().parents[2] / 'computer_products_100.xlsx',
    ]

    workbook_path = None
    for path in candidate_paths:
        if path.exists():
            workbook_path = path
            break

    if workbook_path is None:
        raise FileNotFoundError('ไม่พบไฟล์ computer_products_100.xlsx ใน workspace')

    workbook = openpyxl.load_workbook(workbook_path, data_only=True)
    worksheet = workbook.active

    products = []
    for row in worksheet.iter_rows(min_row=2, values_only=True):
        if not any(cell is not None and str(cell).strip() for cell in row):
            continue

        name, brand_name, category_name, description, price = row[:5]
        if not name:
            continue

        products.append((
            str(name),
            str(brand_name),
            str(category_name),
            str(description or ''),
            int(price or 0),
        ))

    return products


PRODUCTS = load_products_from_excel()


class Command(BaseCommand):
    help = 'เพิ่มข้อมูลสินค้าคอมพิวเตอร์จากไฟล์ Excel ลงฐานข้อมูล (รันซ้ำได้ ไม่สร้างข้อมูลซ้ำ)'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for name, brand_name, category_name, description, price in PRODUCTS:
            brand, _ = Brand.objects.get_or_create(name=brand_name)
            category, _ = Category.objects.get_or_create(name=category_name)

            product, created = Product.objects.update_or_create(
                name=name,
                defaults={
                    'brand': brand,
                    'category': category,
                    'description': description,
                    'price': price,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'เสร็จสิ้น: เพิ่มใหม่ {created_count} รายการ, อัปเดต {updated_count} รายการ '
            f'(Brand {Brand.objects.count()}, Category {Category.objects.count()}, '
            f'Product {Product.objects.count()})'
        ))
