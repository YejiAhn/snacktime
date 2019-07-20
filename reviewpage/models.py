from django.db import models
from django.utils import timezone
#from faker import Faker
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.CharField(max_length=256)
    photo = models.ImageField(blank=True)
    CATEGORY_CODES = (
        ('00', 'undefined'),

        ('10', 'icecream'),
        ('11', 'icecream_bar'),
        ('12', 'icecream_cone'),

        ('20', 'liquid'),
        ('21', 'liquid_coffee'),
        ('22', 'liquid_dairy'),
        ('23', 'liquid_soda'),

        ('30', 'snack'),

        ('40', 'sweets'),
        ('41', 'sweets_chocolate'),
        ('42', 'sweets_candy'),
        ('43', 'sweets_gum'),
        ('44', 'sweets_jelly'),

        ('50', 'convenient'),
        ('51', 'convenient_gimbab'),
        ('52', 'convenient_sandwich'),
        ('53', 'convenient_dosirak'),

        ('60', 'ramen'),

        ('70', 'alcohol'),
        ('71', 'alcohol_beer'),
        ('72', 'alcohol_soju'),

        ('80', 'bread/dessert'),
        ('81', 'dessert_bread'),
        ('82', 'dessert_cake'),

        ('90', 'etc'),
    )
    category_code = models.CharField(max_length=2, choices=CATEGORY_CODES)

    # PBstore = models.ImageField(blank=True)  # img필드 수정 필요

    PB_STORE_CODES = (
        ('0', 'is_not_pb'),
        ('1', 'cu'),
        ('2', 'gs25'),
        ('3', 'emart24'),
        ('4', 'seveneleven'),
        ('5', 'ministop'),
    )
    pb_store_code = models.CharField(max_length=1, choices=PB_STORE_CODES)

    emoticon = models.ImageField(blank=True, upload_to='products_photos',
                                 default='https://image.flaticon.com/icons/png/128/1742/1742384.png')

    rating = models.FloatField(null=True, blank=True, default=0.0)
    num_rating = models.IntegerField(default=0)

    rank_point = models.FloatField(null=True, blank=True, default=0)

    saved_users = models.ManyToManyField(
        User, blank=True, related_name='products_saved', through='Save')

    def update_emoticon(self):  # 나중에 수정할 때 씀
        if self.rating >= 0.0 and self.rating <= 1.0:
            self.emoticon = 'https://image.flaticon.com/icons/png/128/1742/1742482.png'
        elif self.rating > 1.0 and self.rating <= 2.0:
            self.emoticon = 'https://image.flaticon.com/icons/png/128/1742/1742328.png'
        elif self.rating > 2.0 and self.rating <= 3.0:
            self.emoticon = 'https://image.flaticon.com/icons/png/128/1742/1742373.png'
        elif self.rating > 3.0 and self.rating <= 4.0:
            self.emoticon = 'https://image.flaticon.com/icons/png/128/1742/1742324.png'
        elif self.rating > 4.0 and self.rating <= 5.0:
            self.emoticon = 'https://image.flaticon.com/icons/png/128/1742/1742356.png'

        self.save()

    def update_date(self):  # 나중에 수정할 때 씀
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-rank_point']


class Review(models.Model):
    # id는 자동 추가
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    REVIEW_RATINGS = (
        (1, '우웩'),
        (2, '노맛'),
        (3, '그닥'),
        (4, '맛나'),
        (5, '꿀맛'),
    )
    review_rating = models.IntegerField(choices=REVIEW_RATINGS)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to='review_photos')
    liked_users = models.ManyToManyField(
        User, blank=True, related_name='reviews_liked', through='Like')

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
