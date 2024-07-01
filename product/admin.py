from django.contrib import admin
from .models import  Role, Product, Services, Order_product , Order_Services


admin.site.register(Role)
admin.site.register(Services)
admin.site.register(Order_product)
admin.site.register(Order_Services)

admin.site.register(Product)






