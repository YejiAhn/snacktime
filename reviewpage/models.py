from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import numpy as np
# Create your models here.
from faker import Faker
from random import randint

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

    rating = models.FloatField(null=True, blank=True, default=0)

    rank_point = models.FloatField(null=True, blank=True, default=0)

    saved_users = models.ManyToManyField(
        User, blank=True, related_name='products_saved', through='Save')


    def update_emoticon(self):  # 나중에 수정할 때 씀
        if self.review_set.all().count() == 0:
            self.emoticon = 'https://image.flaticon.com/icons/svg/1742/1742373.svg'
            self.rating = "리뷰 없음"
        elif self.rating > 0.0 and self.rating <= 1.0:
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
    
    def get_rating(self):
        review_list = self.review_set.all()
        sum_rating = 0.0
        if review_list.count()>0 :
            for review in review_list:
                sum_rating += review.review_rating
            product_rating = sum_rating / review_list.count()
        else : product_rating = 0.0
        self.rating = round(product_rating,2)
        self.save()

    ### 수정: 랭크포인트 정해주는 함수. activate function-sigmoid(임시)
    def calc_rank_point(self):
        threshold= 5 # 최소 댓글수에 해당하는 값. 임시로 5로 설정.
        num_reviews = self.review_set.all().count()
        self.rank_point = self.rating*(1/1+np.exp(-num_reviews+threshold))
        self.save()

    def update_rate(self): 
        ### 수정: 빼기로 했던 듯?
        # self.updated_at = timezone.now()
        self.get_rating()
        self.update_emoticon()
        self.calc_rank_point()
        self.save()

    def seed(self,count,taste):
        myfake = Faker('ko_KR')
        if taste == 'good':
            for i in range(count):
                Review.objects.create(
                    product=self,
                    content=myfake.text(),
                    review_rating=randint(3,5), ### 과제: 이 부분이 막힘
                    # author=User.objects.filter(username = 'test_user') 
                )
        elif taste == 'soso':
            for i in range(count):
                Review.objects.create(
                    product=self,
                    content=myfake.text(),
                    review_rating=randint(2,4),
                    # author=User.objects.filter(username = 'test_user')
                )
        elif taste == 'bad':
            for i in range(count):
                Review.objects.create(
                    product=self,
                    content=myfake.text(),
                    review_rating=randint(1,3),
                    # author=User.objects.filter(username = 'test_user')
                )
        self.update_rate()


    def __str__(self):
        return self.name

    ### 과제: 정렬하기 순서를 바꾸는 방법은? 편의점 필터 못 만듦.
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

    def __product__(self):
        return self.product
    
    ### 수정: 랜덤 리뷰 생성 (개수, 상품id, ['good', 'soso', 'bad'])

    ### 수정3 : review 정렬하기. 일단은 임시로 updated_at 순으로 정했다.
    class Meta:
        ordering = ['-updated_at']
    ###


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
