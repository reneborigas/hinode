from django.contrib import admin

# Register your models here.
from .models import ReviewProgram
# class programAdmin(admin.ModelAdmin):
#     class Meta:
#         model=program
class ReviewProgramAdmin(admin.ModelAdmin):
    class Meta:
          model=ReviewProgram
          

    
# admin.site.register(program,programAdmin)

admin.site.register(ReviewProgram,ReviewProgramAdmin)

 