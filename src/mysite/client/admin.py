from django.contrib import admin
from .models import WXUser, WrongQuestions, ListOfQuestion, history

# Register your models here.

admin.site.register(WXUser)
admin.site.register(WrongQuestions)
admin.site.register(ListOfQuestion)
admin.site.register(history)