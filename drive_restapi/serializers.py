from rest_framework import serializers

# import DB models
from .models import users
from .models import currentusers
from .models import members

class usersSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = '__all__'

# 1. 현재 들어오는 차량
class currentusersSerializer(serializers.ModelSerializer):
    class Meta:
        model = currentusers
        fields = '__all__'

# 2. 기존 멤버십 고객
class membersSerializer(serializers.ModelSerializer):
    class Meta:
        model = members
        fields = '__all__'