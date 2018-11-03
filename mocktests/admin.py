from django.contrib import admin

# Register your models here.
from .models import MockTest,MockTestSection,MockTestSubSection
# class programAdmin(admin.ModelAdmin):
#     class Meta:
#         model=program
 
class MockTestAdmin(admin.ModelAdmin):
    class Meta:
          model=MockTest

class MockTestSectionAdmin(admin.ModelAdmin):
    class Meta:
          model=MockTestSection

class MockTestSubSectionAdmin(admin.ModelAdmin):
    class Meta:
          model=MockTestSubSection



                
 
admin.site.register(MockTest,MockTestAdmin)
admin.site.register(MockTestSection,MockTestSectionAdmin)
admin.site.register(MockTestSubSection,MockTestSubSectionAdmin)
