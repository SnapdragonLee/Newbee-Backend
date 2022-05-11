from django.contrib import admin
from .models import WXUser, WrongQuestions, ListOfQuestion, history, done_question, UserApproveSolution

# Register your models here.

admin.site.register(WXUser)
admin.site.register(WrongQuestions)
admin.site.register(ListOfQuestion)
admin.site.register(UserApproveSolution)
admin.site.register(history)
admin.site.register(done_question)
