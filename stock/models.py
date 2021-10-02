from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import pre_save
from .utils import unique_slug_generator

User  = get_user_model()

# Create your models here.
class Stock(models.Model):
    name  = models.CharField(max_length=120,blank=False,null=False)
    price = models.IntegerField(blank=False,null=False)
    slug  = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name

class Stock_Query(models.Model):
    stock  = models.ForeignKey(Stock,on_delete=models.CASCADE,blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=False,null=False)
    query  = models.CharField(max_length=120,blank=True, unique=False)

    def __str__(self):
        return self.query


def stock_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(stock_pre_save_receiver, sender=Stock)