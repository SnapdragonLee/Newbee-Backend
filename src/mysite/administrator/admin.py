from django.contrib import admin
from .models import Question, SubQuestion, Solution

admin.site.register(Question)
admin.site.register(SubQuestion)
admin.site.register(Solution)