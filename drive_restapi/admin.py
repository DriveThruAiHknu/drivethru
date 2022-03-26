from django.contrib import admin

# Register your models here.
from .models import prod
from .models import today_user
from .models import member
from .models import cafe
from .models import login
from .models import receipt
from .models import item

admin.site.register(prod)
admin.site.register(today_user)
admin.site.register(member)
admin.site.register(cafe)
admin.site.register(receipt)
admin.site.register(login)
admin.site.register(item)
