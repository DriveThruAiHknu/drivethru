from django.db import models

# Create your models here.

class cafe(models.Model):
    managerPassword = models.IntegerField(primary_key=True)
    staffPassword = models.IntegerField()

class login(models.Model):
    loginID = models.IntegerField(primary_key=True)
    password = models.IntegerField()

class members(models.Model):
    memberID = models.AutoField(primary_key=True)
    memberCar = models.TextField(max_length=10)
    memberName = models.TextField(max_length=10)

    def __str__(self):
        return self.memberName

class todayUsers(models.Model):
    todayUserID = models.AutoField(primary_key=True)
    todayUserCar = models.TextField(max_length=10)

    def __str__(self):
        return self.todayUserCar

class orders(models.Model):
    orderID = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    memberID = models.ForeignKey(members, on_delete=models.CASCADE, db_column="memberID") # 알아서 PK 참조
    todayUserID = models.ForeignKey(todayUsers, on_delete=models.CASCADE, db_column="todayUserID") # 알아서 PK 참조
    orderPrice = models.IntegerField()
    orderDate = models.DateTimeField(auto_now_add=True) # 처음 생성시 한번만 자동입력
    orderTodayID = models.IntegerField() #오류나서 int로 바꿈

class prods(models.Model):
    prodID = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    prodCategory = models.TextField(max_length=10)
    prodName = models.TextField(max_length=10)
    prodPrice = models.IntegerField()
    prodImage = models.ImageField(blank = True) # 경로 지정 필요 /prodImage/ URL 추가 필요
    prodRecommend = models.BooleanField()
    prodHotOrCold = models.IntegerField()
    prodCafAmount = models.BooleanField()
    prodSyrup = models.IntegerField() # 0 false 1 true 취급
    prodShot = models.BooleanField()
    prodMilk = models.BooleanField()
    prodWhip = models.BooleanField()
    prodJavaChip = models.BooleanField()
    prodDriz = models.BooleanField()
    prodSalesRate = models.IntegerField()

class items(models.Model):
    itemID = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    orderID = models.ForeignKey(orders, on_delete=models.CASCADE, db_column="orderID") # 알아서 PK 참조
    prodID = models.ForeignKey(prods, on_delete=models.CASCADE, db_column="prodID") # 알아서 PK 참조
    itemQuantity = models.IntegerField()
    itemSize = models.IntegerField()
    itemPrice = models.IntegerField()
    itemHotOrCold = models.IntegerField()
    itemCafAmount = models.IntegerField()
    itemSyrup = models.IntegerField()
    itemShot = models.IntegerField()
    itemMilk = models.IntegerField()
    itemWhip = models.IntegerField()
    itemJavaChip = models.IntegerField()
    itemDriz = models.IntegerField()