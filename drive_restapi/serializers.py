from rest_framework import serializers

# import DB models
from .models import todayUsers
from .models import members

# 1. 현재 들어오는 차량
class todayUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = todayUsers
        fields = '__all__'

# 2. 기존 멤버십 고객
class membersSerializer(serializers.ModelSerializer):
    class Meta:
        model = members
        fields = '__all__'