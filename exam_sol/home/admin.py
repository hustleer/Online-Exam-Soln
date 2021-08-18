from django.contrib import admin
from home.models import  CustomUser,  QuestionAnwers

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['pidit', 'question', 'answer', 'status' ]
    fields = ('question', 'answer', 'status')

admin.site.register(CustomUser )
admin.site.register(QuestionAnwers,QuestionAnswerAdmin) 


