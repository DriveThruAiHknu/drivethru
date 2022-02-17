from django.db import models

# Create your models here.

class membership(models.Model):
    userID = models.AutoField(primary_key=True)
    userName = models.TextField(max_length=10)
    userCar = models.TextField(max_length=10)

class order(models.Model):
    orderID = models.AutoField(primary_key=True)
    totalPrice = models.IntegerField
    userID = models.ForeignKey(membership, on_delete=models.CASCADE, db_column="userID") # 알아서 PK 참조

class prod(models.Model):
    prodID = models.AutoField(primary_key=True)
    category = models.TextField(max_length=10)
    prodName = models.TextField(max_length=10)
    prodPrice = models.IntegerField
    prodImage = models.ImageField(blank = True) # 경로 지정 필요 /prodImage/ URL 추가 필요

class prodOptionDetail(models.Model):
    prodOptionDetailID = models.AutoField(primary_key=True)
    prodID = models.ForeignKey(prod, on_delete=models.CASCADE, db_column="prodID") # 알아서 PK 참조
    hot = models.IntegerField
    iced = models.IntegerField
    icedAmount = models.IntegerField
    cafAmount = models.IntegerField
    syrupVanila = models.IntegerField
    syrupHazel = models.IntegerField
    syrupCaramel = models.IntegerField
    syrupMocha = models.IntegerField
    syrupFrap = models.IntegerField
    shot = models.IntegerField
    wholeMilk = models.IntegerField
    lawFatMilk = models.IntegerField
    nonFatMilk = models.IntegerField
    soyMilk = models.IntegerField
    oatMilk = models.IntegerField
    whipNormal = models.IntegerField
    whipEspresso = models.IntegerField
    javaChip = models.IntegerField
    DrizChoco = models.IntegerField
    DrizCaramel = models.IntegerField

class orderDetail(models.Model):
    orderdetailID = models.AutoField(primary_key=True)
    orderID = models.ForeignKey(order, on_delete=models.CASCADE, db_column="orderID") # 알아서 PK 참조
    prodID = models.ForeignKey(prod, on_delete=models.CASCADE, db_column="prodID") # 알아서 PK 참조
    quantity = models.IntegerField
    size = models.IntegerField
    price = models.IntegerField
    orderHot = models.IntegerField
    orderIced = models.IntegerField
    ordericedAmount = models.IntegerField
    ordercafAmount = models.IntegerField
    ordersyrupVanila = models.IntegerField
    ordersyrupHazel = models.IntegerField
    ordersyrupCaramel = models.IntegerField
    ordersyrupMocha = models.IntegerField
    ordersyrupFrap = models.IntegerField
    ordershot = models.IntegerField
    orderwholeMilk = models.IntegerField
    orderlawFatMilk = models.IntegerField
    ordernonFatMilk = models.IntegerField
    ordersoyMilk = models.IntegerField
    orderoatMilk = models.IntegerField
    orderwhipNormal = models.IntegerField
    orderwhipEspresso = models.IntegerField
    orderjavaChip = models.IntegerField
    orderDrizChoco = models.IntegerField
    orderDrizCaramel = models.IntegerField







