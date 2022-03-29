from django.db import models

# Create your models here.

class cafe(models.Model):
    manager_password = models.IntegerField(primary_key=True)
    staff_password = models.IntegerField()

class login(models.Model):
    login_id = models.IntegerField(primary_key=True)
    password = models.IntegerField()
    
class member(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_car = models.TextField(max_length=10)
    member_name = models.TextField(max_length=10)

    def __str__(self):
        return self.member_name

class today_user(models.Model):
    today_user_id = models.AutoField(primary_key=True)
    today_user_car = models.TextField(max_length=10)

    def __str__(self):
        return self.today_user_car

class receipt(models.Model):
    receipt_id = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    member_id = models.ForeignKey(member, on_delete=models.CASCADE, db_column="memberID") # 알아서 PK 참조
    today_user_id = models.ForeignKey(today_user, on_delete=models.CASCADE, db_column="todayUserID") # 알아서 PK 참조
    receipt_price = models.IntegerField()
    receipt_date = models.DateTimeField(auto_now_add=True) # 처음 생성시 한번만 자동입력
    receipt_today_id = models.IntegerField() #오류나서 int로 바꿈

class prod(models.Model):
    prod_id = models.AutoField(primary_key=True) # 자동으로 1씩 증가하는 값
    prod_category = models.TextField(max_length=10)
    prod_name = models.TextField(max_length=20)
    prod_price = models.IntegerField()
    prod_image = models.ImageField(blank = True) # 경로 지정 필요 /prodImage/ URL 추가 필요
    prod_recommend = models.BooleanField()
    prod_hot_cold = models.IntegerField() #0 베이커리 1 hot 2 cold 3 hot & cold
    prod_caf_amount = models.BooleanField()
    prod_syrup = models.IntegerField() # 0 false 1 true 취급
    prod_shot = models.BooleanField()
    prod_milk = models.BooleanField()
    prod_whip = models.BooleanField()
    prod_java_chip = models.BooleanField()
    prod_driz = models.BooleanField()
    prod_sales_rate = models.IntegerField()

    def __str__(self):
        return self.prod_name

class item(models.Model):
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