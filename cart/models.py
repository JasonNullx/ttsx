from django.db import models
from goods.models import *
from users.models import Users

# Create your models here.


class CartInfo(models.Model):
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    user = models.ForeignKey(Users)

