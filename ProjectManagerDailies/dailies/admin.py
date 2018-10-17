from django.contrib import admin

from .models import *

admin.site.register(Contractor)
admin.site.register(Employee)
admin.site.register(Employee_Report)
admin.site.register(Equipment)
admin.site.register(Equipment_Report)
admin.site.register(Report)
admin.site.register(Project)
# class ChoiceInline(admin.TabularInline):
#     model = Choice
#     extra = 3
#
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
#     list_display = ('question_text', 'pub_date', 'was_published_recently')
#
# admin.site.register(Question, QuestionAdmin)
