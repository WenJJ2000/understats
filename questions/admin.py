from django.contrib import admin

# Register your models here.
from .models import DecisionTreeNode

admin.site.register(DecisionTreeNode)
