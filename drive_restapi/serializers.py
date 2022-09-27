from rest_framework import serializers

# import DB models
from .models import today_user
from .models import member
from .models import prod
from .models import receipt
from .models import item
from .models import login

# 1. 현재 들어오는 차량
class todayUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = today_user
        fields = '__all__'

# 2. 기존 멤버십 고객
class membersSerializer(serializers.ModelSerializer):
    class Meta:
        model = member
        fields = '__all__'

#4. 영수증
class receiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = receipt
        fields = '__all__'

#5. 영수증 아이템
class itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = item
        fields = '__all__'

# a. 현재 메뉴 목록
class prodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = prod
        fields = '__all__'

# b. 로그인
class loginsSerializer(serializers.ModelSerializer):
    class Meta:
        model = login
        fields = '__all__'

