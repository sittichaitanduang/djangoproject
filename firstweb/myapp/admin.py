from django.contrib import admin
from .models import Member,Phone,Product

admin.site.register(Member)
admin.site.register(Phone)
class PhoneAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'brand',
        'model_name',
        'price',
        'stock',
        'is_available',
        'created_at',
    )

    search_fields = (
        'brand',
        'model_name',
    )

    list_filter = (
        'brand',
        'is_available',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "detail")
    search_fields = ("title",)