from rest_framework import serializers

# import DB models
from .models import today_user
from .models import member
from .models import prod

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

# a. 현재 메뉴 목록
class prodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = prod
        fields = '__all__'