from django.contrib import admin
from .models import WXUser, WrongQuestions, ListOfQuestion

# Register your models here.

admin.site.register(WXUser)
admin.site.register(WrongQuestions)
admin.site.register(ListOfQuestion)