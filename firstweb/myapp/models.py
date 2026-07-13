from django.db import models


class Member(models.Model):
  name = models.CharField(max_length=100)
  tel = models.CharField(max_length=50)
  email = models.EmailField()
  point = models.IntegerField(default=1)
  address = models.TextField(null=True, blank=True)

  def __str__(self):
    #return self.name + " (คะแนน : " + str(self.point) + " points)"
    return 'ชื่อ: {0}, คะแนน: {1}'.format(self.name, self.point)

class Phone(models.Model):
    brand = models.CharField(max_length=100)      #ยี่ห้อ
    model_name = models.CharField(max_length=200) #ชื่อรุ่น
    price = models.DecimalField(                  #เก็บราคา
        max_digits=10,
        decimal_places=2
    )
    stock = models.IntegerField(default=0)      #จำนวนสินค้า
    description = models.TextField()              #รายละเอียดมือถือ
    is_available = models.BooleanField(default=True) #สินค้าเปิดขายไหม
    created_at = models.DateTimeField(auto_now_add=True) #เวลาสร้างข้อมูล

    def __str__(self):
        return f"{self.brand} {self.model_name}"
    
class Product(models.Model):
       title = models.CharField(max_length=255, verbose_name="ชื่อสินค้า")
       detail = models.TextField(verbose_name="รายละเอียด", null=True, blank=True)
       image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="รูปภาพ")
       others = models.CharField(null=True, blank=True, verbose_name="อื่นๆ")

       def __str__(self):
          return self.title


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, null=True, blank=True,verbose_name="ชื่อ")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="รูปโปรไฟล์")
    bio = models.TextField(null=True, blank=True, verbose_name="ข้อมูลส่วนตัว")
    website = models.URLField(null=True, blank=True, verbose_name="เว็บไซต์")

    def __str__(self):
        return f'{self.user.username} - {self.fullname} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
       instance.profile.save()


from django.contrib import admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
   list_display = ("user", "fullname", "avatar", "bio", "website")
   search_fields = ("user__username", "fullname")
