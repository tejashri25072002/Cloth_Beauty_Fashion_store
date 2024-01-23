from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class cloth_product(models.Model):
    name=models.CharField(max_length=50,verbose_name="product name")
    price=models.FloatField()
    pdetails=models.CharField(max_length=100,verbose_name="product details")
    CAT=((1,'One Piece'),(2,'Lehengas'),(3,'Sarees'),(4,'Suits'),(5,'Shirts'),(6,'Jeans'),(7,'Crop Tops'),(8,'Daily Wear'))
    cat=models.IntegerField(verbose_name="category",choices=CAT)
    OCCA=((1,'Anniversary'),(2,'Birthday Party'),(3,'Bachelorette Party'),(4,'Independence Day'),(5,'Wedding'),(6,'Daily Wear'))
    occa=models.IntegerField(verbose_name="occassion",choices=OCCA)
    is_active=models.BooleanField(default=True,verbose_name="Available")
    pimage=models.ImageField(upload_to='image')

    #def __str__(self):
    #    return self.name

class AddCart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(cloth_product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    pid=models.ForeignKey(cloth_product,on_delete=models.CASCADE,db_column="pid")
    quantity=models.IntegerField(default=1)

class Contact(models.Model):
    name=models.CharField(max_length=50,verbose_name="contactor name")
    email=models.CharField(max_length=50,verbose_name="contactor email")
    message=models.CharField(max_length=500,verbose_name="contactor message")

class customer_details(models.Model): 
    uname=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    firstname=models.CharField(max_length=50,null=True)
    lastname=models.CharField(max_length=50,null=True)
    mobile=models.BigIntegerField(null=True)
    address=models.CharField(max_length=350,null=True)
    is_active=models.BooleanField(default=True, verbose_name ="Active")