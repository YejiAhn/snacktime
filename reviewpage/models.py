from django.db import models
from django.utils import timezone
#from faker import Faker
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.IntegerField()
    rating = (
        ('1', '우웩'),
        ('2', '노맛'),
        ('3', '그닥'),
        ('4', '맛나'),
        ('5', '꿀맛'),
    )
    is_PB = models.BooleanField()
    #category = 
    saved_users = models.ManyToManyField(User, blank=True, related_name='products_liked', through='Save')

class Review(models.Model):
    # id는 자동 추가
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    photo = models.ImageField(blank=True, upload_to='review_photos')
    liked_users = models.ManyToManyField(User, blank=True, related_name='reviews_liked', through='Like')

    def update_date(self):
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.id


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self): 
        return 'id=%d, user id=%d' % (self.id, self.user.id)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):  
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):  
    instance.profile.save()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Save(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)