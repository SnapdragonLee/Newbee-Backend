from django.contrib import admin

from basic.user import WXUser
from basic.questions import Question, SubQuestion, Solution

# Register your models here.

admin.site.register(WXUser)
admin.site.register(Question)
admin.site.register(SubQuestion)
admin.site.register(Solution)
