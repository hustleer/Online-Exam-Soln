from django.contrib import admin
from home.models import  CustomUser,  QuestionAnwers , Images

class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ['pidit', 'question', 'answer', 'status' ]
    fields = ('question', 'answer', 'status')


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['pidit' , 'image_tag' , 'id' , ]
    fields = ('pidit' , 'image' ,  )

    
admin.site.register(CustomUser )
admin.site.register(Images,ImagesAdmin) 
admin.site.register(QuestionAnwers,QuestionAnswerAdmin) 


