# coding:utf-8
from django.db import models
from users.models import Users
from goods.models import GoodsInfo

# Create your models here.


class OrderInfo(models.Model):
    oid = models.CharField(max_length=20, primary_key=True)    #时间+用户编号
    user = models.ForeignKey(Users)
    odate = models.DateTimeField(auto_now_add=True)
    oIsPay = models.BooleanField(default=False)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150)


class OrderDetailInfo(models.Model):
    goods = models.ForeignKey(GoodsInfo)
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()

