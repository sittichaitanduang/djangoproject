from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        images = [
            '/media/products/iPhone-17-Air.jpg',
            '/media/products/messageImage_1765029937578.jpg',
            '/media/products/1757672591_iPhone-17-Pro-Cosmic-Orange-Back.png',
            '/media/products/GSMN-APL-17PM256OR_1_260326_090407.webp',
            '/media/products/s-l1600.webp',
        ]
        if self.pk is None:
            return images[0]
        return images[self.pk % len(images)]

    def __str__(self):
        return f'{self.name} - {self.price:,.0f} บาท'
