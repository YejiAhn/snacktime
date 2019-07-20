from django.db import models

# Create your models here.

from django.utils import timezone 
# from faker import Faker
from django.contrib.auth.models import User
# from django.db.models.signals import post_save 
# from django.dispatch import receiver


class Product(models.Model):
    name= models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    photo = models.ImageField(blank=True)
    category = models.CharField(max_length=256)
    PBstore = models.ImageField(blank=True)
    emoticon = models.ImageField(blank=True, upload_to='products_photos', default='https://image.flaticon.com/icons/png/128/1742/1742384.png')
    rating = models.FloatField(null=True, blank=True, default=0.0)
    num_rating = models.IntegerField(default=0)
    rank_point = models.FloatField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)

    liked_users = models.ManyToManyField(User, blank=True, related_name='products_liked', through='Like')

    def update_emoticon(self): # 나중에 수정할 때 씀
        self.updated_at = timezone.now()
        if self.rating >=0.0 and self.rating <=1.0:
            self.emoticon='https://image.flaticon.com/icons/png/128/1742/1742482.png'
        elif self.rating >1.0 and self.rating <=2.0:
            self.emoticon='https://image.flaticon.com/icons/png/128/1742/1742328.png'
        elif self.rating >2.0 and self.rating <=3.0:
            self.emoticon='https://image.flaticon.com/icons/png/128/1742/1742373.png'
        elif self.rating >3.0 and self.rating <=4.0:
            self.emoticon='https://image.flaticon.com/icons/png/128/1742/1742324.png'
        elif self.rating >4.0 and self.rating <=5.0:
            self.emoticon='https://image.flaticon.com/icons/png/128/1742/1742356.png'

        self.save()
    
    def update_date(self): # 나중에 수정할 때 씀
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-rank_point']

    # def decide_ranking(*category):
    #     if category != None:
    #         products=Product.objects.all().filter(category=category)
    #     else:
    #         products=Product.objects.all()
    #     products = products.
        


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
