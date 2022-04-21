from django.contrib import admin
from .models import Question, SubQuestion

admin.site.register(Question)
admin.site.register(SubQuestion)