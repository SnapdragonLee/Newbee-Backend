from django.contrib import admin
from models.basic.questions import Question, SubQuestion, Solution, AdminApproveSolution

admin.site.register(AdminApproveSolution)
admin.site.register(Question)
admin.site.register(SubQuestion)
admin.site.register(Solution)
