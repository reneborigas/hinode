from django.db import models

# Create your models here.

from tinymce.models import HTMLField
from programs.models import ReviewProgram

class Lesson(models.Model):
    title=models.CharField(max_length = 200) 
    subtitle = models.TextField(null=True)
    overview =HTMLField()
    description =HTMLField()
    reviewprogram = models.ForeignKey(ReviewProgram,on_delete=models.CASCADE)
    ACTIVE = 1
    INACTIVE = 0
    
    STATUS_CHOICES = (  
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        
    )
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE,
    ) 

    deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title   
 
