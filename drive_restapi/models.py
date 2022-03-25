from django.db import models

# Create your models here.

class cafe(models.Model):
    managerPassword = models.IntegerField(primary_key=True)
    staffPassword = models.IntegerField()

class login(models.Model):
    loginID = models.IntegerField(primary_key=True)
    password = models.IntegerField()
<<<<<<< HEAD

<<<<<<< HEAD
class member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_car = models.TextField(max_length=10)
    member_name = models.TextField(max_length=10)

    def __str__(self):
        return self.member_name

class today_user(models.Model):
    today_user_id = models.AutoField(primary_key=True)
    today_user_car = models.TextField(max_length=10)
=======
=======

>>>>>>> a0b2b0e45b50005aebc8e5eb58ea4c0fab8e66d3
class members(models.Model):
    memberID = models.AutoField(primary_key=True)
    memberCar = models.TextField(max_length=10)
    memberName = models.TextField(max_length=10)

    def __str__(self):
        return self.memberName

class todayUsers(models.Model):
    todayUserID = models.AutoField(primary_key=True)
    todayUserCar = models.TextField(max_length=10)
<<<<<<< HEAD
>>>>>>> a0b2b0e45b50005aebc8e5eb58ea4c0fab8e66d3

    def __str__(self):
        return self.todayUserCar

<<<<<<< HEAD
class receipt(models.Model):
    receipt_id = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    member_id = models.ForeignKey(member, on_delete=models.CASCADE, db_column="memberID") # 알아서 PK 참조
    today_user_id = models.ForeignKey(today_user, on_delete=models.CASCADE, db_column="todayUserID") # 알아서 PK 참조
    receipt_price = models.IntegerField()
    receipt_date = models.DateTimeField(auto_now_add=True) # 처음 생성시 한번만 자동입력
    receipt_today_id = models.IntegerField() #오류나서 int로 바꿈
=======

    def __str__(self):
        return self.todayUserCar
>>>>>>> a0b2b0e45b50005aebc8e5eb58ea4c0fab8e66d3

class prod(models.Model):
    prod_id = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    prod_category = models.TextField(max_length=10)
    prod_name = models.TextField(max_length=10)
    prod_price = models.IntegerField()
    prod_image = models.ImageField(blank = True) # 경로 지정 필요 /prodImage/ URL 추가 필요
    prod_recomment = models.BooleanField()
    prod_hot_cold = models.IntegerField()
    prod_caf_amount = models.BooleanField()
    prod_syrup = models.IntegerField() # 0 false 1 true 취급
    prod_shot = models.BooleanField()
    prod_milk = models.BooleanField()
    prod_whip = models.BooleanField()
    prod_java_chip = models.BooleanField()
    prod_driz = models.BooleanField()
    prod_sales_rate = models.IntegerField()
=======
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
>>>>>>> a0b2b0e45b50005aebc8e5eb58ea4c0fab8e66d3

class items(models.Model):
    item_id = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    receipt_id = models.ForeignKey(receipt, on_delete=models.CASCADE, db_column="orderID") # 알아서 PK 참조
    prod_id = models.ForeignKey(prod, on_delete=models.CASCADE, db_column="prodID") # 알아서 PK 참조
    item_quantity = models.IntegerField()
    item_size = models.IntegerField()
    item_price = models.IntegerField()
    item_hot_cold = models.IntegerField()
    item_caf_amount = models.IntegerField()
    item_syrup = models.IntegerField()
    item_shot = models.IntegerField()
    item_milk = models.IntegerField()
    item_whip = models.IntegerField()
    item_java_chip = models.IntegerField()
    item_driz = models.IntegerField()